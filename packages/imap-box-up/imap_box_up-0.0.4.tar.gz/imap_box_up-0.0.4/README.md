# imap_box_up

[![Documentation Status](https://readthedocs.org/projects/imap/badge/?version=latest)](https://imap.readthedocs.io/en/latest/?badge=latest)

**[imap_box_up](https://imap.readthedocs.io/en/latest/)** is a tool for visualize and convert format of the hd-map. This project was inspired by Apollo, modified by [imap](https://github.com/daohu527/imap/releases/tag/v0.1.7), the imap tool is very useful. 

The name of **imap_box_up** , Just to modified from imap_box

The modified tool is named **imap_box_up** just to distinguish it from **imap_box**

imap_box_up source code: [https://github.com/porterpan/imap_box_up](https://github.com/porterpan/imap_box_up)

**Note:**

- the map road lane attribution should have curb, if not have curb, task will random selection shouler, stop, walking to create apoolo map.

- The project is Modify on project of [https://github.com/daohu527/imap](https://github.com/daohu527/imap)

> I found that imap_box had the problem of inaccurate junction drawing, which could not meet the needs of my project. Therefore, I modified imap_box based on it to adapt to appollo hdmap code. 


## fix junction bug

![valid junction](https://img2.imgtp.com/2024/04/12/aHEcAl7a.png)

**Supported features**:
1. Visualize the hd-map, supported formats: Apollo, OpenDrive.
2. Find lane by id
3. Convert format: Opendrive to Apollo format.

| os      | support                 | remark |
|---------|-------------------------|--------|
| ubuntu  | :heavy_check_mark:      |        |
| mac     | :heavy_check_mark:      |        |
| windows | :heavy_check_mark:      |        |

## Related work
- [odrviewer.io](https://odrviewer.io/) is an excellent interactive online OpenDRIVE viewer.
- [esmini](https://github.com/esmini/esmini) is a basic OpenSCENARIO player.
- [apollo_map](https://github.com/Flycars/apollo_map) convert carla map to apollo

## Quick start

#### Install
You can install imap by following cmd.
```shell
pip3 install imap_box_up
```

## Example
#### 1. Visualization
After the installation is complete, you can view the map with the following command.
```shell
imap_box_up -m data/borregas_ave.txt
// or
imap_box_up -m data/town.xodr
```
Currently supported formats:
* Apollo map
* OpenDrive map

#### 2. Find lane by id
You can use below command to find lane by id, Found lane is shown in **Red**.
```shell
imap_box_up -m data/borregas_ave.txt -l lane_35
```

#### 3. Format conversion
Now you can convert OpenDrive map to Apollo map by following command.

- save as utm world coordinates(**world map** for old feature)
```shell
imap_box_up -f -i data/town.xodr -o data/apollo_map.txt
```

- save as inertial system coordinates (**relative map** for new feature)

```shell
imap_box_up -f -r -i data/town.xodr -o data/apollo_map.txt
```

#### 4. junction display Format

junction display with road shape

```shell
imap_box_up -f -r -i data/town.xodr -o data/apollo_map.txt
```

![junction detail](https://img2.imgtp.com/2024/04/12/Ct9V2l51.png)

junction display with box shape

```shell
imap_box_up -f -r -b -i data/town.xodr -o data/apollo_map.txt
```

![junction error](https://imap.readthedocs.io/en/latest/_images/map_show.jpg)



The following is the display of the hd-map in `data\borregas_ave.txt`.You can click on the lane you want to display more detail info, which will display the current lane's id, as well as the predecessor and successor lane's id in the upper left corner.

![imap_box_up convert map load to rviz display](https://img2.imgtp.com/2024/04/12/a1QPsCb2.png)


## Questions
1. After running the command `imap_box_up -m data/your_map_file`, nothing display and no errors!!!

A: Check the permissions of the map file, if the current user does not have permissions, modify the permissions with the following commands.
```shell
sudo chmod 777 data/your_map_file
```
2. Map data permission checking has no problem, still nothing display and no errors!
A: It's better to install imap_box by running "sudo pip3 install imap_box", then run "imap -m xxx.txt".

> If you have any questions, please feel free to contact me.