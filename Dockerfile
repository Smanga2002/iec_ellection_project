#Obtain a Jupter notebook that runs on a container
FROM jupyter/minimal-notebook:python-3.11

#Set the working directory
WORKDIR /Users/SmangalisoOageneg/Projects/iec_project

#Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#This is the default command that runs Jupyter Notebook
CMD ["start-notebook.sh"]