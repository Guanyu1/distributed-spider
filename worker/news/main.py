import sys
sys.path.append('../')
import init
import utils.tools as tools
from utils.log import log
from base.spider import Spider
from utils.export_data import ExportData

# 需配置
import news.task_status as task_status
from news.parsers import *

MASTER_ADDRESS = tools.get_conf_value('config.conf', 'master', 'address')
def main():
    while True:
        if task_status.is_doing:
            tools.delay_time(60 * 5)

        task_status.is_doing = True

        # 查找任务
        url = MASTER_ADDRESS + '/update_task'
        tasks = tools.get_json_by_requests(url)

        def begin_callback():
            log.info('\n********** news begin **********')
            # 更新任务状态 doing

            data = {
                'tasks':tasks,
                'status':602
            }

            if tools.get_json_by_requests(url, data = data):
                log.debug('更新任务状态 正在做...')

        def end_callback():
            log.info('\n********** news end **********')
            task_status.is_doing = False

            data = {
                'tasks':tasks,
                'status':602
            }

            if tools.get_json_by_requests(url, data = data):
                log.debug('更新任务状态 已做完！')

        # 配置spider
        spider = Spider(tab_urls = 'news_urls', begin_callback = begin_callback, end_callback = end_callback, parser_params = tasks, delete_tab_urls = True)

        # 添加parser
        spider.add_parser(news_parser)

        spider.start()

if __name__ == '__main__':
    main()