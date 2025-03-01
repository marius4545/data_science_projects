import random
import tkinter as tk
from tkinter import ttk

FAULT_PROBABILITY = 0.1  # 10% that it will be a miss / fault
TOTAL_PINS = 10
FAULT = "F"


def roll_value(roll):
    return 0 if roll == "F" else roll


class BackendBowling:
    def __init__(self):
        self.frames = []

    def reset(self):
        self.frames.clear()

    def simulate_roll(self, available_pins):
        return random.choices(
            ["F", random.randint(0, available_pins)],
            weights=[FAULT_PROBABILITY, 1 - FAULT_PROBABILITY],
        )[0]

    def simulate_frame(self):
        if len(self.frames) >= 10:
            return None
        frame = []
        frame_index = len(self.frames) + 1
        # Frames from 1 to 9
        if frame_index < 10:
            # The first roll
            first_roll = self.simulate_roll(TOTAL_PINS)
            frame.append(first_roll)
            # If it is a strike of 10 pins and no fault, the frame will end.
            if first_roll != "F" and first_roll == 10:
                self.frames.append(frame)
                return frame
            # The second roll: if the first roll was a fault then reset available pins to 10
            available = (
                TOTAL_PINS
                if first_roll == "F"
                else (TOTAL_PINS - roll_value(first_roll))
            )
            second_roll = self.simulate_roll(available)
            frame.append(second_roll)
            self.frames.append(frame)
            return frame
        # 10th Frame
        # The first roll
        first_roll = self.simulate_roll(TOTAL_PINS)
        frame.append(first_roll)
        # The second roll
        if first_roll != "F" and first_roll == 10:
            second_roll = self.simulate_roll(TOTAL_PINS)
        else:
            available = (
                TOTAL_PINS
                if first_roll == "F"
                else (TOTAL_PINS - roll_value(first_roll))
            )
            second_roll = self.simulate_roll(available)
            frame.append(second_roll)
            # Get a extra roll if it's a strike or spare
            if (first_roll != "F" and first_roll == 10) or (
                roll_value(first_roll) + roll_value(second_roll) == 10
            ):
                third_roll = self.simulate_roll(TOTAL_PINS)
                frame.append(third_roll)
            self.frames.append(frame)
            return frame

    def calculate_score(self):
        score = 0
        rolls = []
        for frame in self.frames:
            for roll in frame:
                rolls.append(roll_value(roll))
        roll_index = 0
        for frame_index in range(10):
            if frame_index >= len(self.frames):
                break
            frame = self.frames[frame_index]
            # Frames for 1 to 9
            if frame_index < 9:
                # Strike
                if frame[0] != "F" and frame[0] == 10:
                    bonus1 = rolls[roll_index + 1] if roll_index + 1 < len(rolls) else 0
                    bonus2 = rolls[roll_index + 2] if roll_index + 2 < len(rolls) else 0
                    score += 10 + bonus1 + bonus2
                    roll_index += 1
                # Spare
                elif (
                    len(frame) >= 2
                    and roll_value(frame[0]) + roll_value(frame[1]) == 10
                ):
                    bonus = rolls[roll_index + 2] if roll_index + 2 < len(rolls) else 0
                    score += 10 + bonus
                    roll_index += 2
                else:
                    score += roll_value(frame[0]) + roll_value(frame[1])
                    roll_index += 2
            else:
                # 10th Frame
                score += sum(roll_value(r) for r in frame)
        return score


class FrontendBowling:
    def __init__(self, master):
        self.master = master
        self.master.title("Bowling Simulator")
        self.master.geometry("620x620")
        self.game = BackendBowling()
        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Text(self.master, height=20, width=70)
        self.text.pack(pady=100)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Green.TButton",
            foreground="white",
            background="green",
            font=("Helvetica", 16),
            padding=10,
        )
        style.map("Green.TButton", background=[("active", "dark green")])
        style.configure(
            "Red.TButton",
            foreground="white",
            background="red",
            font=("Helvetica", 16),
            padding=10,
        )
        style.map("Red.TButton", background=[("active", "dark red")])

        self.simulate_button = ttk.Button(
            self.master,
            text="Simulate Frame",
            command=self.simulate_frame,
            style="Green.TButton",
        )
        self.simulate_button.pack(side="left", padx=50, pady=10)

        self.reset_button = ttk.Button(
            self.master, text="Reset", command=self.reset_game, style="Red.TButton"
        )
        self.reset_button.pack(side="right", padx=50, pady=10)

        self.update_display()

    def simulate_frame(self):
        if len(self.game.frames) >= 10:
            return
        self.game.simulate_frame()
        self.update_display()
        if len(self.game.frames) >= 10:
            self.simulate_button.state(["disabled"])

    def reset_game(self):
        self.game.reset()
        self.simulate_button.state(["!disabled"])
        self.update_display()

    def update_display(self):
        self.text.delete("1.0", tk.END)
        display_text = "Bowling Game Simulation:\n\n"
        for i, frame in enumerate(self.game.frames, start=1):
            display_text += f"Frame {i}: {frame}\n"
        display_text += f"\nTotal Score: {self.game.calculate_score()}\n"
        self.text.insert(tk.END, display_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = FrontendBowling(root)
    root.mainloop()
