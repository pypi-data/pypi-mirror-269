from starlette import status as status
import importlib
import os
import shutil
from .tabviz import main


file_in_static_folder = importlib.resources.files('tabviz').joinpath(os.path.join('static', 'example.twbx'))
destination_folder = os.getcwd()
tabviz_folder = os.path.join(destination_folder, 'tabviz')
if not os.path.exists(tabviz_folder):
    os.makedirs(tabviz_folder)
destination_file = os.path.join(tabviz_folder, "example.twbx")
shutil.copy(file_in_static_folder, destination_file)

# def main():
#     tableau_online_signin(site,site_id,token_name,token_secret,api_version)
#     process_file(destination_file)
#     extract_table_contents_from_file(xml_file)
#     extract_table_contents_from_file_for_column(xml_file)
#     replace_data_in_csv(csv_file,dataset)
#     erv = extract_random_values(csv_file)
#     run_generative_model(api_key,erv,table_contents)
#     run_with_api_key(api_key,erv,table_contents_column,xml_column_data)
#     replace_table_contents_with_xml_data(xml_file, xml_Data)
#     replace_table_contents_with_xml_data_for_columns(xml_file,xml_column_data)
#     process_file_repack(tabviz_folder)
#     workbook_name = generate_random_text(5)
#     url = construct_url(site, site_id, workbook_name)
#     publish_workbook(token_name,token_secret, site_id, project_id, workbook_name, path_to_workbook,site)
#     display_tableau_viz(url)

project_id = " "
destination_file = os.path.join(tabviz_folder, "example.twbx")
xml_file = os.path.join(tabviz_folder, "tabviz","example.xml")
dataset = os.path.join(tabviz_folder, "tabviz", "Data", "1vib26g1r4ena71b8a85o12srz3b", "Product.csv")
path_to_workbook = os.path.join(tabviz_folder, "..", "Data.twbx")
table_contents = ""
table_contents_column = ""
xml_column_data = ' '
xml_Data = " "
api_version = '3.22'
path_to_workbook = os.path.join(tabviz_folder, "..", "Data.twbx")

#ENVS
site_id = os.getenv('site_id')
site = os.getenv('site')
token_name = os.getenv('token_name')
token_secret = os.getenv('token_secret')
csv_file = os.getenv('csv')
api_key = os.getenv('api_key')

if __name__ == "__main__":
    lol.main()