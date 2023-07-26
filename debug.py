from database import ScdbIdols, db
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    db.init(os.environ.get('DATABASE'), host=os.environ.get('SERVER'), user=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'))
    for idols in ScdbIdols.select().where(ScdbIdols.birthday == "12/25"):
        print(idols.idol_name)
    pass

if __name__ == "__main__":
    print(os.environ.get("TOKEN"))
    main()