import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Users.db")


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_all_users(self):
        result = self.cursor.execute("SELECT UserID FROM users")
        return [row[0] for row in result.fetchall()]

    def get_waiting_users(self):
        result = self.cursor.execute("SELECT UserID FROM users WHERE IsWaiting = 1")
        return [row[0] for row in result.fetchall()]

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT ID FROM users WHERE UserID = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_status(self, user_id):
        result = self.cursor.execute("SELECT IsWaiting FROM users WHERE UserID = ?", (user_id,))
        return result.fetchone()[0]

    def get_sex(self, user_id):  ## 0 - female, 1 - male
        result = self.cursor.execute("SELECT Sex FROM users WHERE UserID = ?", (user_id,))
        return result.fetchone()[0]

    def get_age(self, user_id):
        result = self.cursor.execute("SELECT Age FROM users WHERE UserID = ?", (user_id,))
        return result.fetchone()[0]

    def get_name(self, user_id):
        result = self.cursor.execute("SELECT Name FROM users WHERE UserID = ?", (user_id,))
        return result.fetchone()[0]

    def get_interests(self, user_id):
        self.cursor.execute("SELECT Interest1, Interest2, Interest3 FROM users WHERE UserID = ?", (user_id,))
        interests = self.cursor.fetchone()
        return chr(10).join(interests) if interests else (None, None, None)

    def update_status(self, user_id, status):  ## Default 1
        self.cursor.execute("UPDATE users SET IsWaiting = ? WHERE UserID = ?", (status, user_id))
        self.conn.commit()

    def update_sex(self, user_id, sex):  ## Не злоупотреблять
        self.cursor.execute("UPDATE users SET Sex = ? WHERE UserID = ?", (sex, user_id))
        self.conn.commit()

    def update_age(self, user_id, age):
        self.cursor.execute("UPDATE users SET Age = ? WHERE UserID = ?", (age, user_id))
        self.conn.commit()

    def update_name(self, user_id, name):
        self.cursor.execute("UPDATE users SET Name = ? WHERE UserID = ?", (name, user_id))
        self.conn.commit()

    def update_interests(self, user_id, interest1, interest2, interest3):
        self.cursor.execute("UPDATE users SET Interest1 = ?, Interest2 = ?, Interest3 = ? WHERE UserID = ?",
                            (interest1, interest2, interest3, user_id))
        self.conn.commit()

    def add_user(self, user_id, sex, age, name, interest1, interest2, interest3):
        self.cursor.execute(
            "INSERT INTO users (UserID, Sex, Age, Name, Interest1, Interest2, Interest3) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, sex, age, name, interest1, interest2, interest3))
        return self.conn.commit()

    def add_dialogue(self, user_id, other_user_id):
        self.cursor.execute("INSERT INTO dialogues (UserID, OtherUserID) VALUES (?, ?)",
                            (user_id, other_user_id))
        self.cursor.execute("INSERT INTO dialogues (UserID, OtherUserID) VALUES (?, ?)",
                            (other_user_id, user_id))
        return self.conn.commit()

    def get_dialogues(self, user_id):
        result = self.cursor.execute("SELECT OtherUserID FROM dialogues WHERE UserID = ?",
                                     (user_id,))
        return [row[0] for row in result.fetchall()]

    def remove_dialogues(self, user_id):
        self.cursor.execute("DELETE FROM dialogues WHERE UserID = ?",
                                     (user_id,))
        self.conn.commit()

    def get_partner(self, user_id):
        self.update_status(user_id, 1)
        self.cursor.execute("""
                    SELECT UserID FROM users 
                    WHERE UserID != ? 
                    AND IsWaiting = 1
                """, (user_id,))
        potential_partners = [row[0] for row in self.cursor.fetchall()]
        best_partner = None
        best_score = -1
        for partner in potential_partners:
            score = 0
            if self.get_sex(partner) == self.get_sex(user_id):
                score += 0.2
            if abs(self.get_age(partner) - self.get_age(user_id)) <= 5:
                score += 0.2
            interests_partner = set(self.get_interests(partner))
            interests_user = set(self.get_interests(user_id))
            common_interests = interests_partner.intersection(interests_user)
            score += len(common_interests)  ## check and debug the formula
            if score > best_score:
                best_score = score
                best_partner = partner
        return best_partner ## Next add_dialodue and update_status

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE UserID = ?", (user_id,))
        self.cursor.execute("DELETE FROM dialogues WHERE UserID = ?", (user_id,))
        self.cursor.execute("DELETE FROM dialogues WHERE OtherUserID = ?", (user_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


BotDB = BotDB(db_path)