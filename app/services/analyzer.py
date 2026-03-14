import time


def run_analysis(project_id: int):
    
    print(f"Starting analysis for project {project_id}")

    # simulate long running analysis
    time.sleep(5)

    print(f"Analysis completed for project {project_id}")