import scrapy
from gushequSpider.items import GushequspiderItem
class GushequSpider(scrapy.Spider):
    def __init__(self):
        pass

    """这是为了爬取招财大牛猫的post信息而开发的
    """

    name = "gushequSpider"
    start_urls = ["http://www.gushequ.com",]
    

    def parse(self, response):
        # 实例化item，必须放在parse方法中
        item = GushequspiderItem()

        if response.url == self.start_urls[0]:
            article_href = response.xpath(r"//article/div/h2/a/@href").extract_first() 
            yield scrapy.Request(str(article_href),callback=self.parse)
        else:
            # post的标题
            item["title"] = response.xpath(r"/html/head/title/text()").extract_first()
            # pots的作者
            item["author"] = response.xpath(r"//span[@class='vcard author']/a[@rel='author']/text()").extract_first()
            # post的出版时间
            item["entry_date_published"] = response.xpath(r"//time[@class='entry-date published']/@datetime").extract_first()
            # post的多媒体正文，不足之处，没有爬下来照片
            item["rich_media_content"] = response.xpath(r"string(//div[@class='entry-content']/div[@id='page-content']//div[@id='js_content'])").extract_first()
            # post的评论区部分，以列表的形式进行存储
            item["discuss_container"] = []
            
            # 先计算该post中的评论个数
            num = len(response.xpath(r"//ul//li[@id]"))
            for i in range(num):
                i += 1
                # 读者的姓名/网名
                discuss_nikenames = response.xpath(r"//ul//li[@id]["+str(i)+r"]/div[@class='discuss_item_hd']/div[@class='user_info']/div[@class='nickname_wrp']/strong[@class='nickname']/text()").extract_first()
                # 读者的评论点赞数
                comment_praise_num = response.xpath(r"//ul//li[@id]["+str(i)+r"]/div[@class='discuss_item_hd']/div[@class='discuss_opr']/span/span[@class='praise_num']/text()").extract_first()                
                # 读者的评论正文
                discuss_comment = response.xpath(r"string(//ul//li[@id]["+str(i)+r"]/div[@class='discuss_message']/div[@class='discuss_message_content'])").extract_first()                
                # 作者的回复正文
                discuss_replys = response.xpath(r"string(//ul//li[@id]["+str(i)+r"]/div[@class='reply_result']/div[@class='discuss_message']/div[@class='discuss_message_content'])").extract_first()            
                # 作者回复点赞数
                replys_praise_num = response.xpath(r"//ul//li[@id]["+str(i)+r"]/div[@class='reply_result']/div[@class='discuss_item_hd']/div[@class='discuss_opr']/span/span/text()").extract_first()
                # 将该评论单元的各个子项以字典的方式进行储存，并添加到评论区部分列表中
                item["discuss_container"].append({"discuss_nikenames":discuss_nikenames,"discuss_comment":discuss_comment,"comment_praise_num":comment_praise_num,"discuss_replys":discuss_replys,"replys_praise_num":replys_praise_num})
                """运行中的注意部分
                1、关于extract()提炼出得是列表，需要[0]
                2、有些extract()[0]会报错：index 超出 range的错误，尽量用extract_first()
                3、scrapy不接受ascii编码的url，需要用str()进行转换格式
                4、学会用/fowllering-sibling::以及..
                5、还需要加强对xpath的学习，对已经抓取的post如何进行随心所欲的检索是解决问题的关键
                """

            yield item

        # 翻页操作
        nav_previous = response.xpath(r"//div[@class='nav-previous']/a/@href").extract_first()
        if nav_previous is not  None:
            yield scrapy.Request(str(nav_previous), callback=self.parse)
        

