# F1 Race Predictor

A small Python project that combines two things I enjoy: **programming and watching Formula 1**.

I built this project to experiment with predicting race results using machine learning and visualizing races with a simple animated track and leaderboard. Because watching F1 is more fun when you can argue about who will win, I decided to let a Random Forest model have a guess too.

## What it does

- Predicts race finishing positions using a machine learning model.
- Uses qualifying positions and available historical performance data.
- Visualizes races with an animated track and leaderboard.
- Gets Formula 1 data through [FastF1](https://docs.fastf1.dev/).

## Built With

Python, FastF1, Pandas, Scikit-learn and Tkinter.

## Run It

```bash
pip install -r requirements.txt
python F1App.py
```

## Inspiration

Inspired by [F1 Race Replay by IAmTomShaw](https://github.com/IAmTomShaw/f1-race-replay).

This is a personal learning project combining my interest in Formula 1 with my interest in programming. The predictions are experimental — even the model cannot predict every safety car, crash, or Ferrari strategy call.

*Not affiliated with Formula 1 or the FIA.*
