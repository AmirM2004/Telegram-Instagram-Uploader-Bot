# Telegram Instagram Uploader Bot

## Overview

A bot that automatically collects posts from Instagram accounts and uploads photos and videos to a Telegram channel.
Manages link tracking and prevents sending duplicates.

---

## Features

* Collects recent posts from specified Instagram users using Instaloader
* Supports images, videos, and multi-media posts
* Sends media to a Telegram channel automatically via Pyrogram
* Tracks successes, errors, and oversized videos
* Admin-only access for controlling the bot
* Supports sending media in groups or individually
* Randomized delays to avoid Telegram rate limits

---

## Database

* Uses SQLite (`database.db`) to store links that have already been sent
* Prevents resending the same content
* Tables are automatically created for link tracking

---

## Configuration

* `api_id`, `api_hash`, and `bot_token` required for Telegram bot
* Channel IDs for sending media must be configured
* Maximum video size can be set (`max_vedio_size`)
* Maximum caption length can be set (`max_caption_size`)
* Waiting times for sending media can be adjusted

---

## Workflow

1. Admin sends a JSON file with Instagram post links to the bot
2. Bot reads the file and prepares the media for sending
3. Media is sent to the target Telegram channel with optional grouping
4. Logs successes, errors, and oversized files
5. Admin can check status or download error logs via commands
