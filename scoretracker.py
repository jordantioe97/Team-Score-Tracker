from tkinter import *
import tkinter.font as font
import sqlite3
from datetime import datetime

root = Tk()
root.title('Score Tracker')
root.geometry("500x500")


def correct():
    conn = sqlite3.connect('scoretracker.db')
    c = conn.cursor()
    c.execute("SELECT team_id, team_name FROM team WHERE active='Y' AND active_turn=1")
    team_turn = c.fetchall()
    team_id = team_turn[0][0]
    team_name = team_turn[0][1]
    c.execute("INSERT INTO score VALUES (:team_id, :points, :date)",
              {
                  'team_id': team_id,
                  'points': '100',
                  'date': datetime.now()
              })
    conn.commit()
    log_Font = font.Font(size=15)
    log_label = Label(root, text=team_name + " scored 100 points!")
    log_label['font'] = log_Font
    log_label.place(x=110, y=380)
    changeTeams(team_id)
    conn.close()
    displayScore()


def wrong():
    conn = sqlite3.connect('scoretracker.db')
    c = conn.cursor()
    c.execute("SELECT team_id, team_name FROM team WHERE active='Y' AND active_turn=1")
    team_turn = c.fetchall()
    team_id = team_turn[0][0]
    team_name = team_turn[0][1]
    c.execute("INSERT INTO score VALUES (:team_id, :points, :date)",
              {
                  'team_id': team_id,
                  'points': '0',
                  'date': datetime.now()
              })
    conn.commit()
    log_Font = font.Font(size=15)
    log_label = Label(root, text=team_name + " scored    0 points!")
    log_label['font'] = log_Font
    log_label.place(x=110, y=380)
    changeTeams(team_id)
    conn.close()
    displayScore()


def displayScore():
    conn = sqlite3.connect('scoretracker.db')
    c2 = conn.cursor()
    c2.execute("SELECT points FROM score WHERE team_id = 1")
    score_records = c2.fetchall()
    score_counter1 = 0
    for record in score_records:
        score_counter1 += record[0]

    c2.execute("SELECT points FROM score WHERE team_id = 2")
    score_records = c2.fetchall()
    score_counter2 = 0
    for record in score_records:
        score_counter2 += record[0]

    score_Font = font.Font(size=13)
    score1_label = Label(root, text=score_counter1)
    score2_label = Label(root, text=score_counter2)
    score1_label['font'] = score_Font
    score2_label['font'] = score_Font
    score1_label.place(x=95, y=110)
    score2_label.place(x=345, y=110)


def changeTeams(team_id):
    conn = sqlite3.connect('scoretracker.db')
    c = conn.cursor()
    c.execute("UPDATE team SET active_turn=1 WHERE active='Y'")
    conn.commit()
    c.execute("UPDATE team SET active_turn=0 WHERE team_id = " + str(team_id))
    conn.commit()

    c.execute("SELECT team_id, team_name FROM team WHERE active='Y' AND active_turn=1")
    team_turn = c.fetchall()
    team_name = team_turn[0][1]

    turn_Font = font.Font(size=15)
    turn_label = Label(root, text="Turn: " + team_name)
    turn_label['font'] = turn_Font
    turn_label.place(x=170, y=200)

    conn.close()


# Main program
conn = sqlite3.connect('scoretracker.db')
c = conn.cursor()

# Title
title_Font = font.Font(size=16)
title_label = Label(root, text="Score Track Generator")
title_label['font'] = title_Font
title_label.place(x=250, y=20, anchor="center")

c.execute("SELECT team_id, team_name FROM team WHERE active='Y'")
records = c.fetchall()
first = records[0][1]
second = records[1][1]

team_Font = font.Font(size=15)
team1_label = Label(root, text=first)
team2_label = Label(root, text=second)
team1_label['font'] = team_Font
team2_label['font'] = team_Font
team1_label.place(x=70, y=80)
team2_label.place(x=320, y=80)
displayScore()
c.execute("SELECT team_id, team_name FROM team WHERE active='Y' AND active_turn=1")
team_turn = c.fetchall()
team_id = team_turn[0][0]
team_name = team_turn[0][1]

turn_Font = font.Font(size=15)
turn_label = Label(root, text="Turn: " + team_name)
turn_label['font'] = turn_Font
turn_label.place(x=170, y=200)

correct_btn = PhotoImage(file='correcticon.png')
correct_icon = Button(root, image=correct_btn, command=correct)
correct_icon.place(x=180, y=280)

wrong_btn = PhotoImage(file='wrongicon.png')
wrong_icon = Button(root, image=wrong_btn, command=wrong)
wrong_icon.place(x=240, y=280)

conn.commit()
c.close()
root.mainloop()
