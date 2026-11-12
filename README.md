# Fuel Log

A one-page food, water and supplement tracker that runs in your phone's browser. Everything is saved on your device and works offline. Food search needs an internet connection.

**Live app:** https://kefirman9000.github.io/fuel-log/

## Features

- **Calorie and macro rings** on Today, with the full Nutrition Facts label one tap away. The label calories, protein, carbs, fat, water and supplements against your daily goals.
- **Profile-based plan:** enter your age, sex, height, weight, activity, goal and training style. The app suggests calorie, protein, carb, fat and water targets (Mifflin-St Jeor plus body-weight ranges) and explains how it got each one.
- **First-run setup** walks new users through their profile, goal and supplements.
- **Add to home screen:** a one-tap install on Android and step-by-step instructions on iPhone. Works offline once installed.
- **Quick-add bar** pinned to the top: add food or water without scrolling.
- **Automatic logging:** type "bagel with avocado and 4 strips bacon" and all three foods go straight in, with Undo. The app only asks when it isn't sure. You can switch to checking every food first.
- **Food search:** type what you ate, like "2 Little Debbie Nutty Buddy" or "Chipotle chicken bowl". The app searches your saved foods, a built-in list of common restaurant items, USDA FoodData Central and Open Food Facts, then multiplies by the servings, pieces or grams you enter.
- **Barcode scanning** with the camera or a photo, or by typing the number.
- **Supplements:** turn on creatine, vitamin D, fish oil, magnesium, electrolytes, a multivitamin, or add your own. Each one has a daily check-off and a 7-day streak, and the app marks which ones suit your profile.
- **Daily suggestions:** protein left (with food ideas), calories left, whether you're on pace for water, and supplements still to take.
- **Meals:** the log groups food into breakfast, lunch, dinner and snacks, each with a food icon. Tap any entry to edit it.
- **Understands everyday typing:** "I had a couple scrambled eggs and toast for breakfast", typos like "avacado", shorthand like "oj" or "pb&j", "16 oz water", "took my creatine", or your own numbers like "protein shake 30g protein 160 cal".
- **Recent foods and copy meals:** one-tap chips for what you ate lately, "Same as yesterday?" chips for meals, and copy any past meal to today.
- **Save a meal:** combine a meal's foods into one item you can log by name.
- **Fiber, sugar and sodium** from the food databases, with fiber and sodium goals.
- **Favorites:** star a food and it's pinned under the search bar for one-tap logging.
- **History tab:** 30-day averages, the 7-day chart, a day-by-day list and CSV export.
- **Goal checklist** at the top of Today: protein, calories, water, fiber and supplements turn green with a check when met, with a time-of-day nudge.
- **Perfect-day streaks:** days where every goal turns green, with their own badges.
- **What fits now:** snack and meal ideas that fill your remaining protein within your calories left, from your favorites, recent foods and a list of good snacks.
- **Read a nutrition label from a photo:** the numbers are filled in for you to check (runs on your phone with Tesseract.js).
- **Streak card** at the top of Today: your day count, the last 7 days, progress to the next badge, and a reminder if your streak is at risk.
- **Streak badges** from your first log up to a full year, plus a water reminder when you fall behind.
- **Stat styles:** show your day as rings, bars or the full Nutrition Facts label.
- **Themes:** auto, light or dark, and six accent colors. Swipe left or right on Today to change the day.
- **Small animations** when you log water, hit a goal or check off a supplement.
- **Backup:** export and import your data as JSON.
- **In-app updates:** the app checks this repo for a newer version and asks before updating.

## Use it

Open the live link on your phone and add it to your home screen. To run it locally, open `index.html` in a browser. Live camera scanning needs https, which GitHub Pages provides.

USDA search uses a shared demo key with a low hourly limit. For heavier use, get a free key at https://api.data.gov/signup and paste it under **Me & goals → Food search**.

The nutrition targets are estimates, not medical advice.

## Support

If Fuel Log helps you, please consider [sponsoring me on GitHub](https://github.com/sponsors/kefirman9000). ♥
