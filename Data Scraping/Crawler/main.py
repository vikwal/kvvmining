from crawlerm import *
import multiprocessing

root = "../../Database/rawdata.db"

if __name__ == '__main__':
    for i in range(1,7):
        p1 = multiprocessing.Process(target=crawler.crawl, args=("Crawler"+str(i), "../HaltePaare/HaltePaareFinal_"+str(i)+".csv", "../../Database/rawdata.db"))
        p1.start()