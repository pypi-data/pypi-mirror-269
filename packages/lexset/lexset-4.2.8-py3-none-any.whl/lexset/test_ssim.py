from review import analysis
from LexsetManager import simulation


dir1 = "D:/github/coco_analysis/5869/"
# dir2 = "D:/github/medtronic/real_img/"



token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkYzVDZUNVFMdTF2bFZrb2NzUVdfOSJ9.eyJpc3MiOiJodHRwczovL2xleHNldC51cy5hdXRoMC5jb20vIiwic3ViIjoibEI1cjNad0JhZjBSc3ZZUVU0RXpCeFpadHBURDM1OGlAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vbGV4c2V0LnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNzAyNTgzODc1LCJleHAiOjE3MDUxNzU4NzUsImF6cCI6ImxCNXIzWndCYWYwUnN2WVFVNEV6QnhaWnRwVEQzNThpIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.ooqoMsLQCx-WklnWVVbvKcuAP61lvBbSUmGiIxP0B93jWCXxuupdN9rbARzsT-tqzRbFkNnnGih4Qf6LxHcQiDPYo41iWS8xaiTaGE0GTzlFupuZnftG2EAAuqEsWpGVPcgV_GNTDBUJ0o1Amj6C9sNV0dQmr6J2OMxK8tu6PZD8YnnPQ_M_ycZQlsGmJVupUYrF73BPkmPFSYiK8E79oEdsHSPgPZCjuPo4ffmihmWXyU213SoS3HyImvB-ibRmC_3HeFBY_YKmYw9g67Af4WfvQaCbr-bf-Z3OK77f3cUefajK8fFZHTprX1QBAbM-7Y0G3ePrOgNWmD2iLCqJLA"
userID = "3"
organizationID = 1

sim = simulation(token, userID, organizationID)

simulationID = 67890
sim.get_organization_simulations("COMPLETED")
# sim.setSimulation_id(simulationID)

# sim.get_dataset_id()

# # Create an instance of the 'analysis' class
#sample_data = analysis(dir1)
# #sample_data.compare_ssim_distributions(compare_dir=dir2,target_size=(256, 256))
# sample_data.calculate_FID(compare_dir=dir2)
#sample_data.plot_pixel_intensity_distribution()

# from lexset.LexsetManager import merge_datasets

# # Define the directories containing your COCO JSON files and images
# json_dirs = ["D:/github/combine_coco_data/16744", "D:/github/combine_coco_data/16745"]

# # Define the percentage of data to keep from each directory
# percentages = [50, 50]  # 50% from the first directory, 60% from the second

# # Define paths to output JSON and image directory
# output_json_path = "D:/github/combine_coco_data/merge_test_3/coco_annotations.json"
# output_img_dir = "D:/github/combine_coco_data/merge_test_3/"

# # Merge the datasets
# merge_datasets(json_dirs, percentages, output_json_path, output_img_dir)