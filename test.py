import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import unicodedata
import re
import argparse
from datetime import datetime
import schedule

# Ham chuyen doi chu tieng Viet thanh khong dau
def convert_to_ascii(text):
    if not text:
        return ""
    # Chuyen doi dau thanh khong dau
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return text

def get_description(url):
    try:
        # Thêm User-Agent giống trình duyệt
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Tim phan mo ta (thu nhieu loai the khac nhau)
        description = ""
        
        # Thu cac class thuong dung cho mo ta
        classes_to_try = [
            'article__sapo', 
            'entry-sapo',
            'sc-longform-header-sapo',
            'sapo'
        ]
        
        # Tim kiem trong cac class
        for class_name in classes_to_try:
            desc_element = soup.find('div', {'class': class_name})
            if desc_element:
                description = desc_element.text.strip()
                break
        
        # Neu khong tim thay, thu tim the p dau tien sau tieu de
        if not description:
            title_element = soup.find('h1')
            if title_element and title_element.find_next('p'):
                description = title_element.find_next('p').text.strip()
        
        # Chuyen doi sang chu khong dau de hien thi
        ascii_desc = convert_to_ascii(description[:50]) if description else ""
        print(f"Tim thay mo ta: {ascii_desc}..." if description else "Khong tim thay mo ta")
        return description
    except Exception as e:
        print(f"Loi khi lay mo ta: {e}")
        return ""

def get_content(url):
    try:
        # Thêm User-Agent giống trình duyệt
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Tim phan noi dung bai viet
        content_text = ""
        
        # Thu cac class thuong dung cho noi dung
        classes_to_try = [
            'article__body',
            'entry-content',
            'entry entry-no-padding',
            'sc-longform-content',
            'article-content'
        ]
        
        # Tim kiem trong cac class
        for class_name in classes_to_try:
            content_element = soup.find('div', {'class': class_name})
            if content_element:
                # Tim tat ca cac the p (paragraph) trong phan noi dung
                paragraphs = content_element.find_all('p')
                if paragraphs:
                    content_text = '\n'.join([p.text.strip() for p in paragraphs])
                    break
        
        # Neu khong tim thay noi dung, thu tim kiem tat ca cac the p trong trang
        if not content_text:
            all_paragraphs = soup.find_all('p')
            # Loc cac doan van dai hon 30 ky tu (tranh cac doan van ngan va khong lien quan)
            long_paragraphs = [p.text.strip() for p in all_paragraphs if len(p.text.strip()) > 30]
            if long_paragraphs:
                content_text = '\n'.join(long_paragraphs)
        
        print(f"Tim thay noi dung: {len(content_text)} ky tu")
        return content_text
    except Exception as e:
        print(f"Loi khi lay noi dung: {e}")
        return ""

def crawl_baomoi(num_pages=1, articles_per_page=10):
    """
    Lay du lieu tu nhieu trang Baomoi
    
    Args:
        num_pages: So trang can lay
        articles_per_page: So bai viet moi trang
    
    Returns:
        DataFrame chua du lieu da lay
    """
    all_titles = []
    all_links = []
    all_images = []
    all_descriptions = []
    all_contents = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'
    }
    
    for page in range(1, num_pages + 1):
        try:
            # Xac dinh URL cua trang
            if page == 1:
                url = "https://baomoi.com/tin-moi.epi"
            else:
                url = f"https://baomoi.com/tin-moi/trang{page}.epi"
            
            print(f"\nDang lay du lieu trang {page}/{num_pages}")
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all('h3', {'class': 'font-semibold block'})
            
            # Gioi han so bai viet tren moi trang
            article_count = 0
            
            for item in articles:
                if article_count >= articles_per_page:
                    break
                    
                # Lay tieu de va link
                title = item.a.get('title')
                if not title:
                    continue
                    
                link = 'https://baomoi.com' + item.a.get('href')
                
                # Lay hinh anh
                img_tag = item.find('img')
                image = ''
                if img_tag and img_tag.has_attr('src'):
                    image = 'https://baomoi.com' + img_tag.get('src')
                
                # Lay mo ta va noi dung
                ascii_title = convert_to_ascii(title)
                print(f"Bai {article_count+1}: {ascii_title}")
                description = get_description(link)
                content = get_content(link)
                
                # Them vao danh sach
                all_titles.append(title)
                all_links.append(link)
                all_images.append(image)   
                all_descriptions.append(description)
                all_contents.append(content)
                
                # Tang bien dem va tam dung
                article_count += 1
                time.sleep(1)
            
            # Tam dung giua cac trang
            time.sleep(2)
            
        except Exception as e:
            print(f"Loi khi lay du lieu trang {page}: {e}")
            continue
    
    # Tao DataFrame
    df = pd.DataFrame({
        'Tieu de': all_titles,
        'Link': all_links,
        'Anh': all_images,
        'Mo ta': all_descriptions,
        'Noi dung': all_contents,
        'Ngay lay': datetime.now().strftime('%Y-%m-%d')
    })
    
    return df

def save_data(df, output_folder="data"):
    """
    Luu du lieu vao file Excel
    
    Args:
        df: DataFrame chua du lieu
        output_folder: Thu muc dau ra
    
    Returns:
        Duong dan den file Excel
    """
    # Tao thu muc neu chua ton tai
    os.makedirs(output_folder, exist_ok=True)
    
    # Tao ten file voi timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = os.path.join(output_folder, f"baomoi_data_{timestamp}.xlsx")
    
    # Luu vao Excel
    df.to_excel(excel_file, index=False)
    print(f"Da luu du lieu vao file Excel: {excel_file}")
    
    return excel_file


def display_results(df, max_display=5):
    """
    Hien thi ket qua
    
    Args:
        df: DataFrame chua du lieu
        max_display: So bai viet toi da hien thi
    """
    print("\n==== KET QUA ====\n")
    print(f"Tong so bai viet da lay: {len(df)}")
    
    # Hien thi mot so bai viet dau tien
    for i in range(min(max_display, len(df))):
        # Chuyen doi sang chu khong dau de hien thi
        ascii_title = convert_to_ascii(df['Tieu de'][i])
        ascii_desc = convert_to_ascii(df['Mo ta'][i]) if not pd.isna(df['Mo ta'][i]) else "Khong co mo ta"
        ascii_content = convert_to_ascii(df['Noi dung'][i][:150]) if not pd.isna(df['Noi dung'][i]) else ""
        
        print(f"\nBai {i+1}: {ascii_title}")
        print(f"Link: {df['Link'][i]}")
        print(f"Mo ta: {ascii_desc}")
        print(f"Noi dung: {ascii_content}..." if not pd.isna(df['Noi dung'][i]) else "Khong co noi dung")


def schedule_crawler():
    """
    Len lich chay crawler vao 6h sang hang ngay
    """
    def job():
        print(f"\nDang chay crawler luc {datetime.now().strftime('%H:%M:%S')}...")
        df = crawl_baomoi(num_pages=3, articles_per_page=10)
        excel_file = save_data(df)
        print(f"Du lieu da duoc luu vao: {excel_file}")
        print("Hoan thanh!") 

    # Len lich chay luc 6h sang hang ngay
    schedule.every().day.at("06:00").do(job)
    
    print("Crawler da duoc hen gio chay vao 6h sang hang ngay")
    print("Nhan Ctrl+C de dung chuong trinh")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Kiem tra moi phut
    except KeyboardInterrupt:
        print("\nDa dung chuong trinh")


def main():
    """
    Ham chinh
    """
    parser = argparse.ArgumentParser(description='Baomoi Crawler')
    parser.add_argument('--pages', type=int, default=1, help='So trang can lay (mac dinh: 1)')
    parser.add_argument('--articles', type=int, default=10, help='So bai viet moi trang (mac dinh: 10)')
    parser.add_argument('--schedule', action='store_true', help='Len lich chay vao 6h sang hang ngay')
    
    args = parser.parse_args()
    
    if args.schedule:
        schedule_crawler()
    else:
        print(f"Bat dau lay du lieu tu {args.pages} trang, moi trang {args.articles} bai viet")
        df = crawl_baomoi(num_pages=args.pages, articles_per_page=args.articles)
        display_results(df)
        excel_file = save_data(df)
        print(f"Du lieu da duoc luu vao: {excel_file}")
        print("Hoan thanh!")


if __name__ == "__main__":
    main()


