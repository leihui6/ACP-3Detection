/*
    convert *.bin to *.pcd
    input: foldername (contains *.bin point cloud)
    output: output (called "PCD_"+foldername, the filename will not be changed)
    
    
    The reason why we need this tool is supervise.ly requires *.pcd to label instead of *.bin we used before.
*/
#include <fstream>
#include <filesystem>
#include <vector>
#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

namespace fs = std::filesystem;
struct my_pointxyzi
{
	float x, y, z, i;
};

void get_path_in_folder(const std::string & folder, std::vector<std::string> & file_path)
{
	for (const auto & entry : fs::directory_iterator(folder))
	{
		file_path.push_back(entry.path().string());
	}
}

std::string get_only_filename(std::string filename)
{
	size_t start_index = filename.find("\\");
	size_t end_index = filename.find(".");

	return filename.substr(start_index + 1, end_index - start_index - 1);
}

int main(int argc, char * argv[])
{
	if (argc != 2) return -1;

	std::string foldername = std::string(argv[1]);
	std::vector<std::string> filepath_list;
	std::string save_foldername = "PCD_" + foldername;

	get_path_in_folder(foldername, filepath_list);
	if (!std::filesystem::exists(save_foldername))
		std::filesystem::create_directory(save_foldername);
	std::cout << foldername << " contains " << filepath_list.size() << " files" << std::endl;

	int i = 0;
	for (auto & f : filepath_list)
	{
		std::cout << "\r" << "[" << ++i << "/" << filepath_list.size() << "]reading " << f;
		std::ifstream ifile(f, std::ios::binary | std::ios::in);
		if (!ifile.is_open())
		{
			std::cout << "Please check " << f << std::endl;
			return -1;
		}

		my_pointxyzi point;
		pcl::PointCloud<pcl::PointXYZI>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZI>);
		while (ifile.read((char *)&point, sizeof(my_pointxyzi)))
		{
			//std::cout << point.x << " " << point.y << " " << point.z << std::endl;
			pcl::PointXYZI t_p;
			t_p.x = point.x;
			t_p.y = point.y;
			t_p.z = point.z;
			t_p.intensity = point.i;
			cloud->points.push_back(t_p);
		}
		ifile.close();
		std::string currFilenamePcd = save_foldername + "\\" + get_only_filename(f) + ".pcd";
		pcl::io::savePCDFileBinary(currFilenamePcd, *cloud);
	}
	std::cout << "\nAll done" << std::endl;
	return 0;
}
