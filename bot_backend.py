import sqlite3


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `ID` FROM `users` WHERE `UserID` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT `ID` FROM `users` WHERE `UserID` = ?", (user_id,))
        return result.fetchone()[0]

    def get_sex(self, user_id):
        result = self.cursor.execute("SELECT Sex FROM users WHERE UserID = ?", (user_id,))
        return result.fetchone()[0]

    def get_age(self, user_id):
        result = self.cursor.execute("SELECT Age FROM users WHERE UserID = ?", (user_id,))
        return result.fetchone()[0]

    def get_interests(self, user_id):
        self.cursor.execute("SELECT Interesting1, Interesting2, Interesting3 FROM users WHERE UserID = ?", (user_id,))
        interests = self.cursor.fetchone()
        return interests if interests else (None, None, None)

    def add_user(self, user_id, sex, age, name, interesting1, interesting2, interesting3):
        self.cursor.execute(
            "INSERT INTO `users` (`UserID`, `Sex`, `Age`, `Name`, `Interesting1`, `Interesting2`, `Interesting3`) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, sex, age, name, interesting1, interesting2, interesting3))
        return self.conn.commit()

    def add_dialogue(self, user_id, other_user_id):
        self.cursor.execute("INSERT INTO `dialogues` (`UserID`, `OtherUserID`) VALUES (?, ?)",
                            (self.get_user_id(user_id), other_user_id))
        return self.conn.commit()

    def get_dialogues(self, user_id):
        result = self.cursor.execute("SELECT * FROM `dialogues` WHERE `UserID` = ?",
                                     (self.get_user_id(user_id)))
        return result.fetchall()

    def get_partner(self, user_id):
        dialogues = self.get_dialogues(user_id)
        if len(dialogues) == len(self.get_all_users()) - 1:
            print("Вы уже общались со всеми пользователями.")
            return None
        else:
            all_users = self.get_all_users()
            potential_partners = [user for user in all_users if
                                  user[0] != user_id and user[0] not in [dialogue[1] for dialogue in dialogues]]
            best_partner = None
            best_score = -1
            for partner in potential_partners:
                score = 0
                if partner[2] == self.get_user_info(user_id)[2]:  # Проверка пола
                    score += 1
                if abs(partner[3] - self.get_user_info(user_id)[3]) <= 5:  # Проверка возраста
                    score += 1
                interests_partner = set(partner[4:7])
                interests_user = set(self.get_user_info(user_id)[4:7])
                common_interests = interests_partner.intersection(interests_user)
                score += len(common_interests)
                if score > best_score:
                    best_score = score
                    best_partner = partner
            return best_partner

    def get_partner(self, user_id):
        dialogues = self.get_dialogues(user_id)
        if len(dialogues) == len(self.get_all_users()) - 1:
            print("You have already talk with all other users")
            return
        else:
            self.cursor.execute("""
                SELECT * FROM users 
                WHERE UserID != ? 
                AND UserID NOT IN (SELECT OtherUserID FROM dialogues WHERE UserID = ?)
            """, (user_id, self.get_user_id(user_id)))
            potential_partners = self.cursor.fetchall()
            best_partner = None
            best_score = -1
            for partner in potential_partners:
                score = 0
                if partner[2] == self.get_user_info(user_id)[2]:
                    score += 1
                if abs(partner[3] - self.get_user_info(user_id)[3]) <= 5:
                    score += 1
                interests_partner = set(partner[4:7])
                interests_user = set(self.get_user_info(user_id)[4:7])
                common_interests = interests_partner.intersection(interests_user)
                score += len(common_interests)  ## check and debug the formula
                if score > best_score:
                    best_score = score
                    best_partner = partner
            return best_partner

    def close(self):
        self.conn.close()


BotDB = BotDB('Users.db')
