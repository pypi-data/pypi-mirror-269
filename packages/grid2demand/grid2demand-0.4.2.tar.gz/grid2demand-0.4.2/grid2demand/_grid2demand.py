# -*- coding:utf-8 -*-
##############################################################
# Created Date: Thursday, September 28th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import os
from itertools import combinations
import pandas as pd
import shapely
from grid2demand.utils_lib.pkg_settings import pkg_settings
from grid2demand.utils_lib.net_utils import Node, POI, Zone, Agent
from grid2demand.utils_lib.utils import check_required_files_exist

from grid2demand.func_lib.read_node_poi import read_node, read_poi, read_network, read_zone
from grid2demand.func_lib.gen_zone import (net2zone,
                                           sync_zone_and_node_geometry,
                                           sync_zone_and_poi_geometry,
                                           calc_zone_od_matrix)
from grid2demand.func_lib.trip_rate_production_attraction import (gen_poi_trip_rate,
                                                                  gen_node_prod_attr)
from grid2demand.func_lib.gravity_model import run_gravity_model, calc_zone_production_attraction
from grid2demand.func_lib.gen_agent_demand import gen_agent_based_demand

from pyufunc import (path2linux, get_filenames_by_ext, cvt_int_to_alpha,
                     generate_unique_filename)


class GRID2DEMAND:

    def __init__(self, input_dir: str = "", output_dir: str = "",
                 use_zone_id: bool = False, verbose: bool = False) -> None:
        """initialize GRID2DEMAND object

        Args:
            input_dir (str, optional): input directory of your data. Defaults to "".
            output_dir (str, optional): output directory. Defaults to "".
            use_zone_id (bool, optional): whether to use zone_id from node.csv. Defaults to False.
            verbose (bool, optional): print processing message. Defaults to False.
        """

        # check input directory
        if not input_dir:
            self.input_dir = path2linux(os.getcwd())
            print(f"  : Input directory is not specified. \
                  Use current working directory {self.input_dir} as input directory. \
                  Please make sure node.csv and poi.csv are in {self.input_dir}.")
        else:
            self.input_dir = path2linux(input_dir)
        self.output_dir = path2linux(output_dir) if output_dir else self.input_dir

        self.verbose = verbose
        self.use_zone_id = use_zone_id

        # check input directory
        self.__check_input_dir()

        # load default package settings, user can modify the settings before running the model
        self.__load_pkg_settings()

    def __check_input_dir(self) -> None:
        """check input directory

        Raises:
            NotADirectoryError: Error: Input directory _input_dir_ does not exist.
            Exception: Error: Required files are not satisfied. Please check _required_files_ in _input_dir_.

        Returns:
            None: will generate self.path_node and self.path_poi for class instance.
        """

        if self.verbose:
            print("  : Checking input directory...")
        if not os.path.isdir(self.input_dir):
            raise NotADirectoryError(f"Error: Input directory {self.input_dir} does not exist.")

        # check required files in input directory
        dir_files = get_filenames_by_ext(self.input_dir, "csv")
        required_files = pkg_settings.get("required_files", [])

        is_required_files_exist = check_required_files_exist(required_files, dir_files, verbose=self.verbose)
        if not is_required_files_exist:
            raise Exception(f"Error: Required files are not satisfied. Please check {required_files} in {self.input_dir}.")

        self.path_node = path2linux(os.path.join(self.input_dir, "node.csv"))
        self.path_poi = path2linux(os.path.join(self.input_dir, "poi.csv"))
        self.path_zone = ""

        # check optional files in input directory (zone.csv)
        optional_files = pkg_settings.get("optional_files", [])
        is_optional_files_exist = check_required_files_exist(optional_files, dir_files, verbose=False)

        if is_optional_files_exist:
            print(f"  : Optional files: {optional_files} are found in {self.input_dir}.")
            print("  : Optional files could be used in the following steps.")
            self.path_zone = path2linux(os.path.join(self.input_dir, "zone.csv"))

        if self.verbose:
            print("  : Input directory is valid.\n")

    def __load_pkg_settings(self) -> None:
        if self.verbose:
            print("  : Loading default package settings...")
        self.pkg_settings = pkg_settings

        if self.verbose:
            print("  : Package settings loaded successfully.\n")

    @property
    def load_node(self) -> dict[int, Node]:
        """read node.csv file and return node_dict

        Raises:
            FileNotFoundError: Error: File {path_node} does not exist.

        Returns:
            dict[int, Node]: node_dict {node_id: Node}

        Examples:
            >>> from grid2demand import GRID2DEMAND
            >>> gd = GRID2DEMAND(input_dir)
            >>> node_dict = gd.load_node
            >>> node_dict[1]
            Node(id=1, x_coord=121.469, y_coord=31.238, production=0, attraction=0,
            boundary_flag=0, zone_id=-1, poi_id=-1, activity_type= '',
            activity_location_tab='', geometry='POINT (121.469 31.238)'
        """

        if not os.path.exists(self.path_node):
            raise FileNotFoundError(f"Error: File {self.path_node} does not exist.")

        # add zone_id to node_dict if use_zone_id is True
        if self.use_zone_id and "zone_id" not in pkg_settings["node_required_fields"]:
            pkg_settings["node_required_fields"].append("zone_id")

        self.node_dict = read_node(self.path_node, self.pkg_settings.get("set_cpu_cores"), verbose=self.verbose)

        # generate node_zone_pair {node_id: zone_id} for later use
        # the zone_id based on node.csv in field zone_id
        self.__pair_node_zone_id = {
            node_id: self.node_dict[node_id]._zone_id
            for node_id in self.node_dict
            if self.node_dict[node_id]._zone_id != -1
        }

        return self.node_dict

    @property
    def load_poi(self) -> dict[int, POI]:
        """read poi.csv file and return poi_dict

        Raises:
            FileExistsError: Error: File {path_poi} does not exist.

        Returns:
            dict[int, POI]: poi_dict {poi_id: POI}
        """

        if not os.path.exists(self.path_poi):
            raise FileExistsError(f"Error: File {self.path_poi} does not exist.")

        self.poi_dict = read_poi(self.path_poi, self.pkg_settings.get("set_cpu_cores"), verbose=self.verbose)
        return self.poi_dict

    @property
    def load_network(self) -> dict[str, dict]:
        """read node.csv and poi.csv and return network_dict

        Raises:
            FileExistsError: Error: Input directory {input_dir} does not exist.

        Returns:
            dict[str, dict]: network_dict {node_dict: dict[int, Node], poi_dict: dict[int, POI]}
        """

        if not os.path.isdir(self.input_dir):
            raise FileExistsError(f"Error: Input directory {self.input_dir} does not exist.")

        # add zone_id to node_dict if use_zone_id is True
        if self.use_zone_id and "zone_id" not in pkg_settings["node_required_fields"]:
            pkg_settings["node_required_fields"].append("zone_id")

        network_dict = read_network(self.input_dir, self.pkg_settings.get("set_cpu_cores"), verbose=self.verbose)
        self.node_dict = network_dict.get('node_dict')
        self.poi_dict = network_dict.get('poi_dict')

        # generate node_zone_pair {node_id: zone_id} for later use
        # the zone_id based on node.csv in field zone_id
        self.__pair_node_zone_id = {
            node_id: self.node_dict[node_id]._zone_id
            for node_id in self.node_dict
            if self.node_dict[node_id]._zone_id != -1
        }

        return network_dict

    def net2zone(self, node_dict: dict[int, Node], num_x_blocks: int = 10, num_y_blocks: int = 10,
                 cell_width: float = 0, cell_height: float = 0,
                 unit: str = "km") -> dict[str, Zone]:
        """convert node_dict to zone_dict by grid.
        The grid can be defined by num_x_blocks and num_y_blocks, or cell_width and cell_height.
        if num_x_blocks and num_y_blocks are specified, the grid will be divided into num_x_blocks * num_y_blocks.
        if cell_width and cell_height are specified, the grid will be divided into cells with cell_width * cell_height.
        Note: num_x_blocks and num_y_blocks have higher priority to cell_width and cell_height.
              if num_x_blocks and num_y_blocks are specified, cell_width and cell_height will be ignored.

        Args:
            node_dict (dict[int, Node]): node_dict {node_id: Node}
            num_x_blocks (int, optional): total number of blocks/grids from x direction. Defaults to 10.
            num_y_blocks (int, optional): total number of blocks/grids from y direction. Defaults to 10.
            cell_width (float, optional): the width for each block/grid . Defaults to 0. unit: km.
            cell_height (float, optional): the height for each block/grid. Defaults to 0. unit: km.
            unit (str, optional): the unit of cell_width and cell_height. Defaults to "km".
                Options: ["km", "meter", "mile"]
            use_zone_id (bool, optional): whether to use zone_id from node_dict. Defaults to False.

        Returns:
            dict[str, Zone]: zone_dict {zone_name: Zone}
        """
        if self.verbose:
            print("  : Note: net2zone will generate grid-based zones from node_dict. \
                \n  : If you want to use your own zones(TAZs), \
                \n  : please skip this method and use taz2zone() instead. \n")

        print("  : Generating zone dictionary...")
        self.zone_dict, self.node_dict_within_zone = net2zone(node_dict,
                                                              num_x_blocks,
                                                              num_y_blocks,
                                                              cell_width,
                                                              cell_height,
                                                              unit,
                                                              self.use_zone_id,
                                                              verbose=self.verbose)
        self.__pair_zone_id_name = {Zone.id: Zone.name for Zone in self.zone_dict.values()}
        return self.zone_dict

    def taz2zone(self) -> dict[str, Zone]:

        if self.verbose:
            print("  : Note: taz2zone will generate zones from zone.csv (TAZs). \
                    \n  : If you want to use grid-based zones (generate zones from node_dict) , \
                    \n  : please skip this method and use net2zone() instead. \n")

        if self.path_zone:
            if self.verbose:
                print("  : Generating zone dictionary...")
            self.zone_dict = read_zone(self.path_zone, self.pkg_settings.get("set_cpu_cores"))
            self.__pair_zone_id_name = {
                Zone.id: Zone.name for Zone in self.zone_dict.values()}

            return self.zone_dict

        print("  : zone.csv does not exist in your input directory. \
              \n    Please check your input directory. \
              \n    Or you can use net2zone() to generate grid-based zones from node_dict.")
        return None

    def sync_geometry_between_zone_and_node_poi(self, zone_dict: dict = "",
                                                node_dict: dict = "", poi_dict: dict = "") -> dict[str, dict]:
        """synchronize geometry between zone and node/poi.

        Args:
            zone_dict (dict, optional): zone dict generated from net2zone. Defaults to "".
                if not specified, use self.zone_dict.
            node_dict (dict, optional): the node_dict generated from read_node/read_network. Defaults to "".
                if not specified, use self.node_dict.
            poi_dict (dict, optional): the poi_dict generated from read_poi/read_network. Defaults to "".
                if not specified, use self.poi_dict.

        Raises:
            Exception: Error in running _function_name_: not valid zone_dict or node_dict
            Exception: Error in running _function_name_: not valid zone_dict or poi_dict

        Returns:
            dict[str, dict]: {"zone_dict": self.zone_dict, "node_dict": self.node_dict, "poi_dict": self.poi_dict}
        """
        if self.verbose:
            print("  : Synchronizing geometry between zone and node/poi...")

        # if not specified, use self.zone_dict, self.node_dict, self.poi_dict as input
        if not all([zone_dict, node_dict, poi_dict]):
            zone_dict = self.zone_dict
            node_dict = self.node_dict
            poi_dict = self.poi_dict

        # synchronize zone with node
        try:
            zone_node_dict = sync_zone_and_node_geometry(zone_dict, node_dict, self.pkg_settings.get("set_cpu_cores"), verbose=self.verbose)
            zone_dict_add_node = zone_node_dict.get('zone_dict')
            self.node_dict = zone_node_dict.get('node_dict')
        except Exception as e:
            raise Exception(
                f"Error in running {self.sync_geometry_between_zone_and_node_poi.__name__}: \
                  not valid zone_dict or node_dict"
            ) from e

        # synchronize zone with poi
        try:
            zone_poi_dict = sync_zone_and_poi_geometry(zone_dict_add_node,
                                                       poi_dict,
                                                       self.pkg_settings.get("set_cpu_cores"))
            self.zone_dict = zone_poi_dict.get('zone_dict')
            self.poi_dict = zone_poi_dict.get('poi_dict')
        except Exception as e:
            raise Exception(
                f"Error in running {self.sync_geometry_between_zone_and_node_poi.__name__}: \
                  not valid zone_dict or poi_dict"
            ) from e

        return {"zone_dict": self.zone_dict, "node_dict": self.node_dict, "poi_dict": self.poi_dict}

    def calc_zone_od_distance_matrix(self, zone_dict: dict = "") -> dict[tuple, float]:
        """calculate zone-to-zone od distance matrix

        Args:
            zone_dict (dict, optional): the zone dictionary. Defaults to "".
                if not specified, use self.zone_dict.

        Returns:
            dict[tuple, float]: zone_od_matrix {(zone_id1, zone_id2): distance}
        """

        # if not specified, use self.zone_dict as input
        if not zone_dict:
            zone_dict = self.zone_dict

        self.zone_od_dist_matrix = calc_zone_od_matrix(zone_dict,
                                                       self.pkg_settings.get("set_cpu_cores"),
                                                       verbose=self.verbose)
        return self.zone_od_dist_matrix

    def gen_poi_trip_rate(self, poi_dict: dict = "", trip_rate_file: str = "", trip_purpose: int = 1) -> dict[int, POI]:
        """generate poi trip rate for each poi

        Args:
            poi_dict (dict, optional): the poi dictionary. Defaults to "".
                if not specified, use self.poi_dict.
            trip_rate_file (str, optional): the path to trip rate file. Defaults to "".
                if not specified, use self.trip_rate_file.
            trip_purpose (int, optional): the trip purpose. Defaults to 1.

        Returns:
            dict[int, POI]: poi_dict {poi_id: POI}
        """

        # if not specified, use self.poi_dict as input
        if not poi_dict:
            poi_dict = self.poi_dict

        # if usr provides trip_rate_file (csv file), save to self.pkg_settings["trip_rate_file"]
        if trip_rate_file:
            if ".csv" not in trip_rate_file:
                raise Exception(f"  : Error: trip_rate_file {trip_rate_file} must be a csv file.")
            self.pkg_settings["trip_rate_file"] = pd.read_csv(trip_rate_file)

        self.poi_dict = gen_poi_trip_rate(poi_dict, trip_rate_file, trip_purpose, verbose=self.verbose)
        return self.poi_dict

    def gen_node_prod_attr(self, node_dict: dict = "", poi_dict: dict = "") -> dict[int, Node]:
        """generate production and attraction for each node based on poi trip rate

        Args:
            node_dict (dict, optional): Defaults to "". if not specified, use self.node_dict.
            poi_dict (dict, optional): Defaults to "". if not specified, use self.poi_dict.

        Returns:
            dict[int, Node]: the updated node_dict {node_id: Node}
        """

        if not all([node_dict, poi_dict]):
            node_dict = self.node_dict
            poi_dict = self.poi_dict

        self.node_dict = gen_node_prod_attr(node_dict, poi_dict,verbose=self.verbose)
        return self.node_dict

    def calc_zone_prod_attr(self, node_dict: dict = "", zone_dict: dict = "") -> dict[str, Zone]:
        """calculate zone production and attraction based on node production and attraction

        Args:
            node_dict (dict, optional): Defaults to "". if not specified, use self.node_dict.
            zone_dict (dict, optional): Defaults to "". if not specified, use self.zone_dict.

        Returns:
            dict[str, Zone]: the updated zone_dict {zone_name: Zone}
        """
        if not all([node_dict, zone_dict]):
            node_dict = self.node_dict
            zone_dict = self.zone_dict
        self.zone = calc_zone_production_attraction(node_dict, zone_dict, verbose=self.verbose)

        return self.zone

    def run_gravity_model(self, zone_dict: dict = "",
                          zone_od_dist_matrix: dict = "",
                          trip_purpose: int = 1,
                          alpha: float = 28507,
                          beta: float = -0.02,
                          gamma: float = -0.123) -> pd.DataFrame:
        """run gravity model to generate demand

        Args:
            zone_dict (dict, optional): dict store zones info. Defaults to "".
            zone_od_dist_matrix (dict, optional): OD distance matrix. Defaults to "".
            trip_purpose (int, optional): purpose of trip. Defaults to 1.
            alpha (float, optional): parameter alpha. Defaults to 28507.
            beta (float, optional): parameter beta. Defaults to -0.02.
            gamma (float, optional): parameter gamma. Defaults to -0.123.

        Returns:
            pd.DataFrame: the final demand dataframe
        """
        # if not specified, use self.zone_dict, self.zone_od_dist_matrix as input
        if not all([zone_dict, zone_od_dist_matrix]):
            zone_dict = self.zone_dict
            zone_od_dist_matrix = self.zone_od_dist_matrix

        # run gravity model to generate demand
        self.zone_od_dist_matrix = run_gravity_model(zone_dict, zone_od_dist_matrix, trip_purpose, alpha, beta, gamma, verbose=self.verbose)
        self.df_demand = pd.DataFrame(list(self.zone_od_dist_matrix.values()))

        # if use_zone_id is True, generate demand dataframe based on zone_id from node.csv
        if self.use_zone_id:

            # generate comb {(o_node_id, d_node_id)}
            # pair_node_zone_id: node_id and zone_id from node.csv, they are unique pairs
            # comb: all possible combinations of node_id pairs
            # comb: can be seen as all possible zone_id pairs from node.csv
            node_zone_lst = list(self.__pair_node_zone_id.keys())

            # create all possible combinations of node_id pairs
            comb = [(i, j) for i in node_zone_lst for j in node_zone_lst]

            # generate demand_lst to store demand dataframe
            demand_lst = []

            # create demand dictionary
            for pair in comb:
                o_node_id, d_node_id = pair
                o_zone_id = self.node_dict[o_node_id].zone_id  # zone_id from generated zone
                d_zone_id = self.node_dict[d_node_id].zone_id  # zone_id from generated zone

                o_zone_name = self.__pair_zone_id_name[o_zone_id]  # zone_name from generated zone
                d_zone_name = self.__pair_zone_id_name[d_zone_id]  # zone_name from generated zone
                if o_zone_name != d_zone_name:
                    try:
                        dist_km = self.zone_od_dist_matrix[(o_zone_name, d_zone_name)].get('dist_km')
                        volume = self.zone_od_dist_matrix[(o_zone_name, d_zone_name)].get('volume')

                        demand_lst.append(
                            {
                                # "o_node_id": o_node_id,
                                "o_zone_id": self.__pair_node_zone_id[o_node_id],
                                "o_zone_name": self.__pair_node_zone_id[o_node_id],

                                # "d_node_id": d_node_id,
                                "d_zone_id": self.__pair_node_zone_id[d_node_id],
                                "d_zone_name": self.__pair_node_zone_id[d_node_id],
                                "dist_km": dist_km,
                                "volume": volume,
                                "geometry": shapely.LineString([self.node_dict[o_node_id].geometry,
                                                                self.node_dict[d_node_id].geometry])

                            }
                        )

                    except KeyError:
                        dist_km = 0
                        volume = 0

                        if self.verbose:
                            print(f"  : Error: zone_od_dist_matrix does not contain {o_zone_name, d_zone_name}.")
            if demand_lst:
                self.df_demand_based_zone_id = pd.DataFrame(demand_lst)
            else:
                self.df_demand_based_zone_id = pd.DataFrame(columns=["o_zone_id", "o_zone_name",
                                                                     "d_zone_id", "d_zone_name",
                                                                     "dist_km", "volume", "geometry"])
            return self.df_demand_based_zone_id

        return self.df_demand

    def gen_agent_based_demand(self, node_dict: dict = "", zone_dict: dict = "",
                               df_demand: pd.DataFrame = "") -> pd.DataFrame:
        """generate agent-based demand

        Args:
            node_dict (dict, optional): _description_. Defaults to "".
            zone_dict (dict, optional): _description_. Defaults to "".
            df_demand (pd.DataFrame, optional): _description_. Defaults to "".

        Returns:
            pd.DataFrame: the final agent-based demand dataframe
        """

        if not isinstance(df_demand, pd.DataFrame):
            df_demand = self.df_demand

        if not all([node_dict, zone_dict]):
            node_dict = self.node_dict
            zone_dict = self.zone_dict

        self.df_agent = gen_agent_based_demand(node_dict, zone_dict, df_demand=df_demand, verbose=self.verbose)
        return self.df_agent

    @property
    def save_demand(self) -> None:

        if not hasattr(self, "df_demand"):
            print("Error: df_demand does not exist. Please run run_gravity_model() first.")
            return

        path_output = generate_unique_filename(path2linux(os.path.join(self.output_dir, "demand.csv")))

        if self.use_zone_id:
            df_demand_non_zero = self.df_demand_based_zone_id[self.df_demand_based_zone_id["volume"] > 0]
            df_demand_non_zero.to_csv(path_output, index=False)
            print(f"  : Successfully saved demand.csv to {self.output_dir}")
            return None

        df_demand_non_zero = self.df_demand[self.df_demand["volume"] > 0]
        df_demand_non_zero.to_csv(path_output, index=False)
        print(f"  : Successfully saved demand.csv to {self.output_dir}")
        return None

    @property
    def save_agent(self) -> None:

        if not hasattr(self, "df_agent"):
            print("Error: df_agent does not exist. Please run gen_agent_based_demand() first.")
            return

        path_output = generate_unique_filename(path2linux(os.path.join(self.output_dir, "agent.csv")))
        self.df_agent.to_csv(path_output, index=False)
        print(f"  : Successfully saved agent.csv to {self.output_dir}")

    @property
    def save_zone(self) -> None:

        if not hasattr(self, "zone_dict"):
            print("Error: zone_dict does not exist. Please run sync_geometry_between_zone_and_node_poi() first.")
            return

        path_output = generate_unique_filename(path2linux(os.path.join(self.output_dir, "zone.csv")))
        zone_df = pd.DataFrame(self.zone_dict.values())
        zone_df.to_csv(path_output, index=False)
        print(f"  : Successfully saved zone.csv to {self.output_dir}")

    @property
    def save_zone_od_dist_table(self) -> None:

        if not hasattr(self, "zone_od_dist_matrix"):
            print("Error: zone_od_dist_matrix does not exist. Please run calc_zone_od_distance_matrix() first.")
            return

        path_output = generate_unique_filename(path2linux(os.path.join(self.output_dir, "zone_od_dist_table.csv")))
        zone_od_dist_table_df = pd.DataFrame(self.zone_od_dist_matrix.values())
        zone_od_dist_table_df = zone_od_dist_table_df[["o_zone_id", "o_zone_name", "d_zone_id", "d_zone_name", "dist_km", "geometry"]]
        zone_od_dist_table_df.to_csv(path_output, index=False)
        print(f"  : Successfully saved zone_od_dist_table.csv to {self.output_dir}")

    @property
    def save_zone_od_dist_matrix(self) -> None:

        if not hasattr(self, "zone_od_dist_matrix"):
            print("Error: zone_od_dist_matrix does not exist. Please run calc_zone_od_distance_matrix() first.")
            return

        path_output = generate_unique_filename(path2linux(os.path.join(self.output_dir, "zone_od_dist_matrix.csv")))

        zone_od_dist_table_df = pd.DataFrame(self.zone_od_dist_matrix.values())
        zone_od_dist_table_df = zone_od_dist_table_df[["o_zone_id", "o_zone_name", "d_zone_id", "d_zone_name", "dist_km", "geometry"]]

        zone_od_dist_matrix_df = zone_od_dist_table_df.pivot(index='o_zone_name', columns='d_zone_name', values='dist_km')

        zone_od_dist_matrix_df.to_csv(path_output)
        print(f"  : Successfully saved zone_od_dist_matrix.csv to {self.output_dir}")

    @property
    def save_node_within_zone(self):
        if not hasattr(self, "node_dict_within_zone"):
            print("Error: node_dict_within_zone does not exist. Please run net2zone() first.")
            return

        path_output = generate_unique_filename(path2linux(os.path.join(self.output_dir, "node_within_zone.csv")))
        node_within_zone_df = pd.DataFrame(self.node_dict_within_zone.values())
        node_within_zone_df.to_csv(path_output, index=False)
        print(f"  : Successfully saved node_within_zone.csv to {self.output_dir}")