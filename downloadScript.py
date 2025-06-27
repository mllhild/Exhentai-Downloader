import os
import sys
import time
import re
import random
import requests
from bs4 import BeautifulSoup

# --- Setup ---
current_directory = os.getcwd()
print(current_directory)
with open('GalleriesToDownload.txt', 'r') as file:
    lines = file.readlines()
if not lines:
    print("Error: GalleriesToDownload.txt is empty.")
    exit(1)

BASE_URL = "https://exhentai.org"
while lines:
    GALLERY_URL = lines.pop(0).strip()  # removes the first element and returns it, then remove any trailing newline or spaces


    # --- Required Cookies (Get from your browser after logging in) ---
    # you need to be logged in to exhentai and have the cookie extension to get these values
    # https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en-US
    COOKIES = {
        'ipb_member_id': '870684',
        'ipb_pass_hash': 'e6856e62b5c6e095369a9dac0660573c',
        'igneous': '3cor7814melin91ij'
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0'
    }

    session = requests.Session()
    session.cookies.update(COOKIES)
    session.headers.update(HEADERS)



    # --- Step 1: Fetch Gallery Page ---
    res = session.get(GALLERY_URL)
    if res.status_code == 200:
        print("Page exists and is reachable.")
    else:
        print(f"Page not reachable, status code: {response.status_code}")

    soup = BeautifulSoup(res.content, 'html.parser')
    ## Print the entire parsed HTML
    #print(soup.prettify())  # This formats the HTML nicely






    # --- Step 2: Get Gallery Meta Data ---
    # Find all td elements with class gdt2
    td_elements = soup.select('div#gmid div#gd3 div#gdd td.gdt2')

    # Get the 6th one (index 5) and extract the number
    pages_text = td_elements[5].text.strip()
    num_pages = int(pages_text.split()[0])
    print(f"{num_pages} images")
    # get other meta data
    post_date = td_elements[0].text.strip()
    print(post_date)
    post_language = td_elements[3].text.strip()
    print(post_language)
    size = td_elements[4].text.strip()
    print(size)

    # get tag list
    taglist_table = soup.find('div', id='taglist')
    gt_divs = taglist_table.find_all('div', class_=True)

    gt_ids = [div['id'] for div in gt_divs]
    for gt_id in gt_ids:
        print(gt_id)
    # get category
    target_div = soup.select_one('div#gmid div#gd3 div#gdc div')
    if target_div:
        category = target_div.text.strip()
        print(category)
        
    # get name
    title_element_gj = soup.find('h1', id='gj')
    if title_element_gj:
        title_gj = title_element_gj.text.strip()
        print(title_gj)
    title_element_gn = soup.find('h1', id='gn')
    if title_element_gn:
        title_gn = title_element_gn.text.strip()
        print(title_gn)

    if title_gn:
        title = title_gn
    elif title_gj:
        title = title_gj
    else:
        title = GALLERY_URL

    print(title)
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
    print(safe_title)

    # create save path directory
    download_path = os.path.join(current_directory, "downloads", safe_title)
    os.makedirs(download_path, exist_ok=True)
    download_path_meta = os.path.join(download_path, "meta")
    os.makedirs(download_path_meta, exist_ok=True)

    #save meta data
    #tags
    with open(os.path.join(download_path_meta, "tags.txt"), 'w', encoding='utf-8') as f:
        for tag_id in gt_ids:
            f.write(tag_id + '\n')
    print(f"Saved tags")
    #metadata
    info = {
        "GALLERY_URL": GALLERY_URL,
        "Title_GJ": locals().get("title_GJ", None),
        "Title_GN": locals().get("title_GN", None),
        "Safe Title": safe_title,
        "Category": category,
        "Post Date": post_date,
        "Language": post_language,
        "Size": size,
        "Number of Pages": num_pages,
    }

    with open(os.path.join(download_path_meta, "meta.txt"), 'w', encoding='utf-8') as f:
        for key, val in info.items():
            f.write(f"{key}: {val}\n")
    print(f"Saved Meta data")











    # --- Step 3: Get Gallery Pages ---
    # Find the table with class 'ptt'
    table = soup.find('table', class_='ptt')

    # Find all <a> tags inside the table
    page_links = table.find_all('a')

    # Extract the highest page number from the hrefs
    page_numbers = [
        int(a['href'].split('=')[-1])
        for a in page_links
        if '?p=' in a['href']
    ]

    if page_numbers:
        max_page = max(page_numbers) + 1
    else:
        max_page = 1  # default to 1 if no pages found
        
    print(f"{max_page} pages to parse")
    # Build list of all gallery page URLs
    gallery_pages = [f"{GALLERY_URL}?p={i}" for i in range(max_page)]
    for page in gallery_pages:
        print(page)
        
    with open(os.path.join(download_path_meta, "galleryUrls.txt"), 'w', encoding='utf-8') as f:
         for page in gallery_pages:
            f.write(page + '\n')
    print(f"Saved Gallery Page Urls")
        
        
        
        
        

    # --- Step 4: Get Gallery Resized Image page URLs ---
    print()
    all_image_page_urls = []
    for page_url in gallery_pages:
        print()
        print(page_url)
        res = session.get(page_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        gallery_div = soup.find('div', class_='gt200', id='gdt')
        if gallery_div:
            links = gallery_div.find_all('a', href=True)
            for a in links:
                print(a['href'])
                all_image_page_urls.append(a['href'])
        
        time.sleep(random.uniform(4, 6))  # wait 10 seconds before next request


    with open(os.path.join(download_path_meta, "ResizedPageUrls.txt"), 'w', encoding='utf-8') as f:
         for page in all_image_page_urls:
            f.write(page + '\n')
    print(f"Saved Resized Image Page Urls")
    
        # --- Step 4.5: Download Gallery Images ---
    all_gallery_image_urls = []
    all_failed_gallery_image_urls = []
    imagesFailed = 0
    retryAttemps = 0
    imagecounter = 0
    url_count = len(all_image_page_urls)
    for url in all_image_page_urls:
        time.sleep(random.uniform(3, 4))
        res = session.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        i3_div = soup.find('div', id='i3')
        if i3_div:
            img_tag = i3_div.find('img')
            if img_tag and img_tag.has_attr('src'):
                img_url = img_tag['src']
                image_name = os.path.basename(img_url)
                image_path = os.path.join(download_path, image_name)

                max_retries = 5
                for attempt in range(1, max_retries + 1):
                    try:
                        res = session.get(img_url, timeout=10)
                        if res.status_code == 200:
                            with open(image_path, 'wb') as f:
                                f.write(res.content)
                            print(f"Downloaded: {image_name}")
                            all_gallery_image_urls.append(img_url)
                            imagecounter += 1
                            break
                        else:
                            print(f"Attempt {attempt}: Failed to download (status code {res.status_code})")
                    except Exception as e:
                        print(f"Attempt {attempt}: Error downloading {img_url} — {e}")

                    if attempt < max_retries:
                        time.sleep(random.uniform(2, 3))
                        retryAttemps += 1
                    else:
                        print(f"Failed to download after {max_retries} attempts: {img_url}")
                        all_failed_gallery_image_urls.append(img_url)
                        imagesFailed += 1
            else:
                print("Image tag with 'src' not found in div#i3")
        else:
            print("div#i3 not found in the HTML")

    

    with open(os.path.join(download_path_meta, "GalleryImageURLsDownloaded.txt"), 'w', encoding='utf-8') as f:
         for page in all_gallery_image_urls:
            f.write(page + '\n')
    print(f"Saved Gallery Image Urls")
    with open(os.path.join(download_path_meta, "GalleryImageURLsFailed.txt"), 'w', encoding='utf-8') as f:
         for page in all_failed_gallery_image_urls:
            f.write(page + '\n')
    print(f"Saved Failed Gallery Image Urls")
    
    
    # Update Lists
    # Failed
    if imagesFailed >= 1:
        with open(os.path.join(current_directory, "FailedToDownloadGalleries.txt"), 'a', encoding='utf-8') as f:
            f.write(url + '\n')
    # Update ToDownload file
    with open("GalleriesToDownload.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)
    # Update Galleries Downloaded Successfully file
    if imagesFailed == 0:
        with open(os.path.join(current_directory, "DownloadedGalleries.txt"), 'a', encoding='utf-8') as f:
            f.write(url + '\n')
            
    print("Cooldown of 20 to 30 seconds for anti scraping detection")        
    time.sleep(random.uniform(20, 30))

# Rest doesnt work because of GP limit
#     # --- Step 5: Get Gallery Original Image URLs ---
#     all_original_image_urls = []
#     for url in all_image_page_urls:
#         res = session.get(url)
#         soup = BeautifulSoup(res.content, 'html.parser')
#         
#         i6_div = soup.find('div', id='i6')
#         if i6_div:
#             inner_divs = i6_div.find_all('div')
#             if len(inner_divs) >= 3:
#                 third_div = inner_divs[2]
#                 a_tag = third_div.find('a', href=True)
#                 if a_tag:
#                     href = a_tag['href']
#                     print(href)
#                     all_original_image_urls.append(href)
# 
#     with open(os.path.join(download_path_meta, "OriginalImageURLs.txt"), 'w', encoding='utf-8') as f:
#          for page in all_original_image_urls:
#             f.write(page + '\n')
#     print(f"Saved Original Image Urls")


#     # --- Step 6: Download Original Images ---
#     MAX_RETRIES = 5
#     imagesFailed = 0
#     retryAttemps = 0
#     imagecounter = 0
#     failed_urls = []
#     url_count = len(all_original_image_urls)
#     for url in all_original_image_urls:
#         imagecounter += 1
#         image_name = os.path.basename(url)
#         image_path = os.path.join(download_path, image_name)
# 
#         for attempt in range(1, MAX_RETRIES + 1):
#             time.sleep(random.uniform(1, 2))  # Short delay before retry
#             try:
#                 response = session.get(url, timeout=10)
#                 if response.status_code == 200:
#                     with open(image_path, 'wb') as f:
#                         f.write(response.content)
#                     print(f"Downloaded ({imagecounter}/{url_count}): {image_name}")
#                     break  # Exit retry loop on success
#                 else:
#                     print(f"Attempt {attempt}: Failed to download {image_name} (status {response.status_code})")
#             except Exception as e:
#                 print(f"Attempt {attempt}: Error downloading {image_name} - {e}")
#             
#             if attempt < MAX_RETRIES:
#                 time.sleep(random.uniform(2, 3))  # Short delay before retry
# 
#         else:
#             print(f"Failed to download {image_name} after {MAX_RETRIES} attempts.")
#             imagesFailed += 1
#             failed_urls.append(url)
# 
#         # Delay after each successful or failed download attempt
#         time.sleep(random.uniform(4, 5))
        



    
    
exit(1)