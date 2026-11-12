# Fuel Log

A one-page food, water and supplement tracker that runs in your phone's browser. Everything is saved on your device and works offline. Food search needs an internet connection.

**Live app:** https://kefirman9000.github.io/fuel-log/

## Features

- **Nutrition Facts label** shows calories, protein, carbs, fat, water and supplements against your daily goals.
- **Profile-based plan:** enter your age, sex, height, weight, activity, goal and training style. The app suggests calorie, protein, carb, fat and water targets (Mifflin-St Jeor plus body-weight ranges) and explains how it got each one.
- **First-run setup** walks new users through their profile, goal and supplements.
- **Add to home screen:** a one-tap install on Android and step-by-step instructions on iPhone. Works offline once installed.
- **Quick-add bar** pinned to the top: add food or water without scrolling.
- **Food search:** type what you ate, like "2 Little Debbie Nutty Buddy" or "Chipotle chicken bowl". The app searches your saved foods, a built-in list of common restaurant items, USDA FoodData Central and Open Food Facts, then multiplies by the servings, pieces or grams you enter.
- **Barcode scanning** with the camera or a photo, or by typing the number.
- **Supplements:** turn on creatine, vitamin D, fish oil, magnesium, electrolytes, a multivitamin, or add your own. Each one has a daily check-off and a 7-day streak, and the app marks which ones suit your profile.
- **Daily suggestions:** protein left (with food ideas), calories left, whether you're on pace for water, and supplements still to take.
- **Small animations** when you log water, hit a goal or check off a supplement.
- **Backup:** export and import your data as JSON.
- **In-app updates:** the app checks this repo for a newer version and asks before updating.

## Use it

Open the live link on your phone and add it to your home screen. To run it locally, open `index.html` in a browser. Live camera scanning needs https, which GitHub Pages provides.

USDA search uses a shared demo key with a low hourly limit. For heavier use, get a free key at https://api.data.gov/signup and paste it under **Me & goals → Food search**.

The nutrition targets are estimates, not medical advice.

## Support

If Fuel Log helps you, please consider [sponsoring me on GitHub](https://github.com/sponsors/kefirman9000). ♥
