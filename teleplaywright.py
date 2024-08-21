import asyncio
from playwright.async_api import async_playwright

user_list = ['username1', 'username2', 'username3']

target_group = 'https://t.me/your_group_link'

throttle_delay = 60  # Adjust as needed


async def invite_user_to_channel(page, username, group):
    try:
        # Search for the user by username
        await page.goto(f'https://t.me/{username}', wait_until='networkidle')

        # Click on the "Add to group" button
        await page.click('button:has-text("Add to group")')

        # Select the target group/channel and invite
        await page.type('input[placeholder="Search"]', group)
        await page.click(f'text={group}')

        await page.click('button:has-text("Add")')
        print(f"Successfully invited {username}")

    except Exception as e:
        print(f"Failed to invite {username}: {e}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://web.telegram.org/')

        # Wait for manual login
        print("Please log in to Telegram Web manually...")
        await asyncio.sleep(60)

        # Iterate over the user list and invite them to the group/channel
        for username in user_list:
            await invite_user_to_channel(page, username, group=target_group)
            await asyncio.sleep(throttle_delay)

        await browser.close()


# Run the script
asyncio.run(main())
