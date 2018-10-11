# Spider_video

爬取外网的的视频代码

#SpiderData
爬取猫眼票房，反爬虫解析(stonefont)

#解题思路

-  解析网页

    当找到网页上票房的位置时，显示的并不是可读的数字。

    ![](/assets/WeChat%20Screenshot_20181011110220.png)

    可以看到class="stonefont"， 正是因为这个，所以我们看不到数字。接下来我们在网页上ctrl+f查找stonefont，找到如图所示的位置

    ![](/assets/2.png)
    
    其中，.woff文件对我们是有用的，是一种字体，如果想要看具体的字体是什么样子的，下载Font Creator查看。
 
-   将上面的.woff文件中的unicode和可读字体对应
    
    ![](/assets/3.png)
    
    首先我们需要一个现有的字体(base.otf)和上面的下载后的.woff文件(maoyan.woff)
    
    ![](/assets/4.png)
    
    利用上图中的代码， 就可以将上面的.woff文件中的unicode和可读字体对应
    
    
   
-  剩下的具体，请看完整代码
