import scrapy
from ..items import HotelscraperItem

class HotelSpider(scrapy.Spider):
  name = 'hotels'
  start_urls=[
    'https://me.cleartrip.com/hotels/united-states/miami/'
    ]
  
  items = HotelscraperItem()

  amenity_category_list = [
    "General", 
    "Food & Beverage", 
    "Business Services", 
    "Front Desk Services", 
    "Travel", 
    "Recreation", 
    "Kids"
    ]

  amenity_category_dict = {
    "General"             : "general", 
    "Food & Beverage"     : "food_beverage", 
    "Business Services"   : "business_service", 
    "Front Desk Services" : "front_desk_service", 
    "Travel"              : "travel",
    "Recreation"          : "recreation", 
    "Kids"                : "kids", 
    }

  def parse(self, response):
    '''
    Parses the list of hotel page. Utilizes the pasrse2 function for detailed crawling of each Hotel.
    Yield a request to the next page.
    '''
    
    next_page_url = response.css('.next_page::attr(href)').extract_first() 
    hotels_card = response.css('.hotels-card')
    for hotel_card in hotels_card:
        hotel_name       = hotel_card.css('.hotels-name span::text').extract_first()
        hotel_url        = hotel_card.css('.hotels-name a::attr(href)').extract_first()
        hotel_review_num = hotel_card.css('.taReviews::text').extract_first()
        hotel_rating     = hotel_card.css('.hotelMeta span meta::attr(content)').extract_first()
        hotel_price      = hotel_card.css('.HotelBookbtn::text')[2].extract()

        items_meta = {
            'hotel_name'      : hotel_name,
            'hotel_url'       : hotel_url,
            'hotel_review_num': hotel_review_num,
            'hotel_rating'    : hotel_rating,
            'hotel_price'     : hotel_price
        }

        request = response.follow(hotel_url, callback=self.parse2, meta = items_meta) 
        yield request
    if next_page_url is not None:  
        request_to_next_page = response.follow(next_page_url, callback = self.parse)
        yield request_to_next_page

  def parse2(self, response):
    '''
    Parses the Hotel Page. Yields the Items.
    '''
    items_meta = response.meta
  
    self.items['hotel_name']       = items_meta['hotel_name']
    self.items['hotel_url']        = items_meta['hotel_url']
    self.items['hotel_review_num'] = items_meta['hotel_review_num']
    self.items['hotel_rating']     = items_meta['hotel_rating']
    self.items['hotel_price']      = items_meta['hotel_price']

    hotel_info = response.css('div.amenitiesCategory div.hotelDescriptionBottom p::text').extract()
    hotelStats  = response.css('.hotelStats span::text').extract()
    check_in  = hotelStats[0]
    check_out = hotelStats[1]
    self.items['check_in'] = check_in
    self.items['check_out'] = check_out
    if not (len(hotelStats)< 3):
        self.items['rooms'] = hotelStats[2]
    
    amenitiesCategories = response.css('.amenitiesCategory')
    
    for amenityCategory in amenitiesCategories[2:]:
        amenity_category_name = amenityCategory.css('strong::text').extract_first()
        if amenity_category_name in self.amenity_category_list:
          amenity_name = amenityCategory.css('.col8::text').extract()
          self.items[self.amenity_category_dict[amenity_category_name]] = amenity_name
           
    hotel_info = [self.replace_all(inf) for inf in hotel_info]
    self.items['hotel_info'] = hotel_info
    
    yield self.items

  def replace_all(self, text, replacements = {'\t':'', '\n':''}):
    '''
    Replaces the unwanted characters from the provided text
    '''
    for i, j in replacements.items():
        text = text.replace(i, j)
    return text
