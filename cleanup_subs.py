import os
import sys
import shutil
import subprocess

class TempChangeDir(object):
    def __init__(self, target_dir):
        self.target_dir = target_dir

    def __enter__(self):
        self.initial_dir = os.getcwd()
        os.chdir(self.target_dir)

    def __exit__(self, exec_type, exec_value, exec_traceback):
        os.chdir(self.initial_dir)

if __name__=='__main__':
	source_folder = input('Folder containing the uploaded files: ')
	target_folder = input('Folder to store the result: ')

	if not os.path.isdir(source_folder):
		raise FileNotFoundError('No folder with name {} exists.'.format(source_folder))

	if os.path.isdir(target_folder):
		raise FileExistsError('folder with name {} already exists.'.format(target_folder))


	shutil.copytree(source_folder, target_folder)
	os.chdir(target_folder)
	base_dir = os.getcwd()

	for submission_folder in os.listdir('.'):
		if 'onlinetext' in submission_folder:
			shutil.rmtree(submission_folder)
		else:
			clean_folder_name = submission_folder.split('_')[0]
			os.rename(submission_folder, clean_folder_name)
			with TempChangeDir(clean_folder_name):
				submitted_filenames = os.listdir('.')
				if len(submitted_filenames) > 1:
					print('Warning: unrecognized file structure at {}/{}. Leaving the directory as is.'.format(target_folder, submission_folder))
					continue

				submitted_filename = submitted_filenames[0]
				submitted_filepath = os.path.join(clean_folder_name, submitted_filename)

				try:
					if submitted_filename.endswith('.zip'):
						subprocess.check_output('unzip \"{}\" > /dev/null'.format(submitted_filename),
						                        shell=True, stderr = subprocess.STDOUT)
						os.remove(submitted_filename)
					elif submitted_filename.endswith('.rar'):
						subprocess.check_output('unrar x \"{}\" > /dev/null'.format(submitted_filename),
						                        shell=True, stderr = subprocess.STDOUT)
						os.remove(submitted_filename)
					else:
						print('Warning: Submission file {} is neither zip nor rar. Leaving it as is.'.format(submitted_filepath))

				except subprocess.CalledProcessError as e:
					print('Error when extracting {}:'.format(submitted_filepath)) 
					print(e.output)

