from typing import Any, Dict, List, Literal, Optional, Union

import requests

Status = Literal["completed", "pending"]
TasksDict = Dict[str, Status]


class TodoClient:
    """
    A client to interact with a Firebase Realtime Database for managing a to-do list.
    Following are the methods provided:
    - clear(): Clears all tasks from the database.
    - add_task(task: str): Adds a new task to the database.
    - delete_task(task: str): Deletes a task from the database.
    - mark_completed(task: str): Marks a task as completed.
    - get_task_by_status(status: Status): Returns a list of task names matching the given status.
    """

    def __init__(self, dburl: str) -> None:
        self.dburl: str = dburl
        if not self.dburl.endswith("/"):
            self.dburl += "/"

    def clear(self) -> Union[str, Dict[str, Any]]:
        """
        Clears all tasks from the database.
        Returns "Success!" if the operation was successful,
        otherwise returns the error in Dictionary.
        """
        response: requests.Response = requests.delete(f"{self.dburl}tasks.json")
        if response.status_code == 200:
            return "Success!"
        else:
            # return the error message from the Firebase server
            return response.json()

    def add_task(self, task: str) -> Union[str, Dict[str, Any]]:
        """
        Adds a new task to the database.
        Returns "Success!" if the operation was successful, error message string
        if the task already exists, otherwise returns the error in Dictionary.
        """

        all_tasks: Optional[TasksDict] = self._get_tasks_data()
        if all_tasks is None:
            return {"error": "Error in add_task: failed to retrieve existing tasks."}

        if task in all_tasks:
            return f'Error in add_task: task "{task}" already exists!'

        # using PATCH to add without overwriting existing tasks
        response: requests.Response = requests.patch(
            f"{self.dburl}tasks.json", json={task: "pending"}
        )

        if response.status_code == 200:
            return "Success!"
        else:
            return response.json()

    def delete_task(self, task: str) -> Union[str, Dict[str, Any]]:
        """
        Deletes a task from the database.
        Returns "Success!" if the operation was successful, error message string if the task does not exist,
        otherwise returns the error in Dictionary.

        """

        all_tasks: Optional[TasksDict] = self._get_tasks_data()
        if all_tasks is None:
            return {"error": "Error in delete_task: failed to retrieve existing tasks."}

        if task not in all_tasks:
            return f'Error in delete_task: task "{task}" does not exist!'

        response: requests.Response = requests.delete(f"{self.dburl}tasks/{task}.json")
        if response.status_code == 200:
            return "Success!"
        else:
            return response.json()

    def mark_completed(self, task: str) -> Union[str, Dict[str, Any]]:
        """
        Marks a task as completed in the database.
        Returns "Success!" if the operation was successful, error message string if the task does not exist,
        otherwise returns the error in Dictionary.
        """

        all_tasks: Optional[TasksDict] = self._get_tasks_data()
        if all_tasks is None:
            return {
                "error": "Error in mark_completed: failed to retrieve existing tasks."
            }

        if task not in all_tasks:
            return f'Error in mark_completed: task "{task}" does not exist!'

        # using PUT to update the value of the specific task
        response: requests.Response = requests.put(
            f"{self.dburl}tasks/{task}.json", json="completed"
        )
        if response.status_code == 200:
            return "Success!"
        else:
            return response.json()

    def get_task_by_status(self, status: Status) -> Union[List[str], Dict[str, Any]]:
        """
        Return task names matching the given status.
        Returns a list of task names if successful, otherwise returns the error in Dictionary.
        """
        params: Dict[str, str] = {"orderBy": '".value"', "equalTo": f'"{status}"'}
        response: requests.Response = requests.get(
            f"{self.dburl}tasks.json", params=params
        )

        if response.status_code == 200:
            tasks: Optional[TasksDict] = response.json()
            # If tasks are found, return their names (the keys) as a list
            return list(tasks.keys()) if tasks else []
        else:
            return response.json()

    def get_all_tasks(self) -> Union[Optional[TasksDict], Dict[str, Any]]:
        """
        Retrieves all tasks from the database.
        Returns all tasks in a dictionary of task:status pairs if successful,
        Returns None if no tasks exist,
        otherwise returns the error in Dictionary.
        """

        all_tasks: Optional[TasksDict] = self._get_tasks_data()
        if all_tasks is None:
            return {
                "error": "Error in get_all_tasks: failed to retrieve existing tasks."
            }
        return all_tasks if all_tasks else None

    def _get_tasks_data(self) -> Optional[TasksDict]:
        """
        Retrieves all tasks from Firebase.
        Returns the tasks dictionary if successful, empty dictionary if no tasks exist,
        otherwise returns None.
        """
        response: requests.Response = requests.get(f"{self.dburl}tasks.json")
        if response.status_code == 200:
            data: Optional[TasksDict] = response.json()
            return data if data is not None else {}
        return None  # Indicate an error occurred
