from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

from ..models import HostInfo

import datetime

now_time = datetime.datetime.now
SECOND_INTERVAL = 2 # 每次访问需要间隔的秒数
RESTRICT_TOTAL_SECOND = 600 # 封 ip 以后，封的总秒数

# 在 DURING_SECOND 秒内，限制访问次数为：RESTRICT_COUNT 次，如果超出了次数就封 ip RESTRICT_TOTAL_SECOND 秒
DURING_SECOND, RESTRICT_COUNT = (600, 30)


class Md1(MiddlewareMixin):

    def process_request(self, request):

        if request.path.startswith('/tasks/tutorial/'): # 只有这个 path 才会限制
            print(request.path)

            host = request.META.get('REMOTE_ADDR')

            # print('host', host)

            ret, created = HostInfo.objects.get_or_create(host=host)

            if not created:
                now = now_time()
                total_sec = (now - ret.start_time).total_seconds()

                if ret.is_lock: # 如果被限制了 ip
                    remain_sec = int(RESTRICT_TOTAL_SECOND - total_sec) # 剩余被封的秒数
                    if remain_sec >= 0:
                        return HttpResponse('操作过于频繁，ip 被封，请 %d 秒后再试' % remain_sec, status=403)
                    else:
                        ret.is_lock = False
                        ret.count = 0
                        ret.start_time = now
                        ret.last_active_time = now
                        ret.save()
                else:
                    during_sec = (now - ret.last_active_time).total_seconds()
                    ret.count += 1
                    ret.last_active_time = now

                    # 如果第一次访问距现在已经有 DURING_SECOND 时间了，那么重新计时
                    if total_sec > DURING_SECOND:
                        ret.start_time = now
                        ret.count = 1
                    # 第一次访问距现在还没有 DURING_SECOND 时间，看看访问次数有没有超，如果访问次数太多就封 ip
                    elif ret.count > RESTRICT_COUNT:
                        ret.is_lock = True
                        ret.start_time = now # 封 ip 后，start_time 就用于计算已经被封了多久，还有多久可以放出来
                        ret.save()
                        return HttpResponse('操作过于频繁，ip 被封，请 %d 秒后再试' % RESTRICT_TOTAL_SECOND, status=403)

                    ret.save()
                    if during_sec < SECOND_INTERVAL: # 如果操作频繁，小于最少间隔时间
                        return HttpResponse('操作过于频繁，请 %d 秒后再试' % SECOND_INTERVAL, status=403)
