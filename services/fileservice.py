class FileService:
    @staticmethod
    def append_to_file(content, filepath="./data.log"):
        """
        Appends a string to a target file.

        Args:
            content (str): The string to append to the file
            filepath (str): The path to the target file
        """

        with open(filepath, "a", encoding="utf-8") as file:
            file.write(content + "\n")
