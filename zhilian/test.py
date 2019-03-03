# -*- coding: utf-8 -*-
import re
import urllib

position = ['Java开发', 'UI设计师', 'Web前端', 'PHP', 'Python', 'Android', '美工', '深度学习',
            '算法工程师', 'Hadoop', 'Node.js', '数据开发', '数据分析师', '数据架构', '人工智能', '区块链',
            '电气工程师', '电子工程师', 'PLC', '测试工程师', '设备工程师', '硬件工程师', '结构工程师',
            '工艺工程师', '产品经理', '新媒体运营', '运营专员', '淘宝运营', '天猫运营', '产品助理',
            '产品运营', '淘宝客服', '游戏运营', '编辑']

s = '<div class="responsibility pos-common">\n<p class="responsibility-tit pos-tit">\n职位描述\n</p>\n<div class="pos-ul">\n<div>如果你对人类世界正在发生的一切抱有好奇心，如果你对严肃的知识抱有敬畏心，如果你一直注重自我通识教育、希望自身不断成长，那么，欢迎你加入我们！</div><div><br></div><div>我们需要什么样的同行者？</div><div><br></div><div>内容编辑 （全职 2人；兼职、实习生同时在招）</div><div><br></div><div>1.加入我们，你需要做：</div><div>（1）与学术部的同事们共同设计研发严肃而有趣的人文社科类通识教育产品；</div><div>（2）与课程老师进行紧密沟通，保证产品质量</div><div>（3）对制作完成的内容产品（音视频、文字）进行校对、编辑；</div><div><span style="font-weight: 400;">（4）岗位所需的其他常规工作。</span><br></div><div><span style="font-weight: 400;">有严肃知识类文章原创能力者优先考虑。</span></div><div><br></div><div>2.我们需要这样的你：</div><div>（1）术业有专攻，对历史学、法学、经济学、政治学、科学史、哲学、文学诸学科中一门或两门颇有心得；</div><div>（2）专业之外，对人文社科领域亦有涉猎；</div><div>（3）富有责任心，自我要求严格；</div><div>（4）良好的团队协作精神。</div><div><br></div><div>3.你将收获：</div><div>（1）薪酬收入：有竞争力的工资、奖金、出版物版税；</div><div>（2）符合国家规定的五险一金；</div><div>（3）与志同道合的良师益友谈笑风生；</div><div>（4）温馨多元的工作氛围；</div><div>（5）部门馆藏图书无限畅读。</div><div><br></div><div><br></div><div>我们正在做一件什么事？读了以下文字，也许你将有所了解：</div><div><br></div><div><br></div><div>我们需要什么样的知识？</div><div><br></div><div>今天，我们身处一个快速、流动、风险极高的社会，它由科学与技术宰治，人文学科退居象牙塔的小角落。而我们，在应对现实问题之时，要快、要精准、要稳控风险。由此，我们学习知识时，抱以「主义」，少了对智慧的真正渴望。学习成了碎片化学习，知识主体还被生了病，叫作「知识焦虑」。</div><div><br></div><div>这是我们时代的精神症候，它源于互联网时代人文精神的缺席。了解这一状态的各路人马纷纷开出自己的药方：要么是你缺什么给你什么的母爱式知识鸡汤，要么是你什么都不懂什么都不知道的父爱式权威万金油。</div><div><br></div><div>只是开出这些药方的人，本身就没有治好自己的顽症，他们与知识的接受者之间既无平等，亦无交流默契可言。更何况，碎片化学习不可能真正获得知识，就像未经消化的食物不会转换为身体所需的营养，未经心灵熔铸的知识也不是真知识。</div><div><br></div><div>难道互联网时代的判词只有肤浅、俗滥吗？</div><div><br></div><div>我们并不这样认为，我们不能在享受了互联网时代的种种便利好处之后，又无情地嘲笑它、挖苦它。</div><div><br></div><div>我们需要改变，需要苏格拉底式的平等对话与思辨。</div><div><br></div><div>我们更需要以尊重和爱来求知。</div><div><br></div><div>尊重意味着我们要放下偏见，去了解人类智慧的多元特征，拥有一套更包容的世界观；爱意味着我们要拥有希腊哲人爱智慧的激情，不为夸耀自身去求取知识。</div><div><br></div><div>秉持这样的知识愿景，我们希望能以互联网突破时空限制之便，为探求真知的人提供严肃而有趣的人文社科类通识教育产品，去回应时代的诉求，去激励学习者将外在的知识内化为自己的血与肉，去运用知识解决生命中的种种难题，而且是加以批判性地使用。</div><div><br></div><div>目前，我们团队已有40多位当代人文社科 &amp; 科学领域一流名师入驻，为我们的知识产品萃精华，去秕糠。但我们在追求知识的路上，还需更多同伴。</div><div><br></div><div>我们期待热爱知识的你，与我们同行！</div>\n</div>\n<div class="pos-develop">\n<span>展开</span>\n<i class="icon icon-blue-jt"></i>\n</div>\n</div>'

s = re.sub(r'<.*?>','',s)
base_url = 'https://fe-api.zhaopin.com/c/i/sou' \
               '?start={}&pageSize=60&cityId=530&workExperience=-1&education=-1' \
               '&companyType=-1&employmentType=-1&jobWelfareTag=-1' \
               '&kw={}&kt=3'


json_url  ='https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=60&cityId=530&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E7%BC%96%E8%BE%91&kt=3'
parse = urllib.parse.urlparse(json_url)
import re

print(re.sub(r'kw=(.*?)&','kw='+str(10)+'&',json_url))
print(re.findall(r'start=(.*?)&',json_url)[0])
