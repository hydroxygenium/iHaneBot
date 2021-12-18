import sqlite3
import io #to convert image to blob format to insert it to database
# from PIL import Image
conn = sqlite3.connect('UserData.db')
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        registration_date TEXT,
        nickname TEXT NOT NULL,
        school_grade TEXT NOT NULL,
        subjects_user_know TEXT NOT NULL,
        subjects_to_learn TEXT NOT NULL
    )
""")
#  id INTEGER PRIMARY KEY,
# profile_photo BLOB NOT NULL
# add it to the end later when you will be able to handle with photos
conn.commit()



class User:
    """
    this class created to organize user registration
    """
    def __init__(self,
            registration_date: str,
            nickname: str,
            school_grade: str,
            subjects_user_know: list,
            subjects_to_learn: list,
            # profile_photo: Image # uncomment when you will add the photo
        ):
        """
        constructor
        """
        self.registration_date = registration_date
        self.nickname = nickname
        self.school_grade = school_grade
        self.subjects_user_know = subjects_user_know
        self.subjects_to_learn = subjects_to_learn
        # self.profile_photo = profile_photo

    # def convert_image_to_blob(self):
    #     """returning blob file of image"""
    #     image = self.profile_photo
    #     stream = io.BytesIO()
    #     image.save(stream, format="JPEG")
    #     imagebytes = stream.getvalue()

    #     return imagebytes

    def get_user_data(self) -> list:
        """
        to insert data into db
        """
        return (str(
            self.registration_date),
            self.nickname,
            self.school_grade,
            str(self.subjects_user_know),
            str(self.subjects_to_learn)
            # self.convert_image_to_blob()
        )

    def save_to_db(self) -> None:
        """
        to save data in db
        """
        user_data = self.get_user_data()

        cur.execute(
                "INSERT INTO users VALUES(?, ?, ?, ?, ?);",
                user_data,
        )
        conn.commit()
