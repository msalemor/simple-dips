class FileService:
    @staticmethod
    def append_to_file(content, filepath="./data.log") -> None:
        """
        Appends a string to a target file.

        Args:
            content (str): The string to append to the file
            filepath (str): The path to the target file
        """

        with open(filepath, "a", encoding="utf-8") as file:
            file.write(content + "\n")

    @staticmethod
    def delete_file(filepath="./data.log") -> None:
        """
        Deletes the target file.

        Args:
            filepath (str): The path to the target file
        """
        try:
            import os

            os.remove(filepath)
        except FileNotFoundError:
            pass
