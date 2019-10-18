from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

from ..models import HostInfo

import datetime

now_time = datetime.datetime.now
SECOND_INTERVAL = 2 # 每次访问间隔秒数
RESTRICT_TOTAL_SECOND = 600 # 封 ip 总秒数
RESTRICT_COUNT = 30 # 访问次数限制


class Md1(MiddlewareMixin):

    def process_request(self, request):

        if request.path.startswith('/tasks/tutorial/'): # 只有这个 path 才会限制
            print(request.path)

            host = request.META.get('REMOTE_ADDR')

            ret, created = HostInfo.objects.get_or_create(host=host)

            if not created:
                now = now_time()
                total_sec = (now - ret.start_time).total_seconds()

                if ret.is_lock: # 如果被限制了 ip
                    remain_sec = int(RESTRICT_TOTAL_SECOND - total_sec) # 剩余被封的秒数
                    if remain_sec >= 0:
                        return HttpResponse('操作过于频繁，%d 秒后再试' % remain_sec, status=403)
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

                    if total_sec > RESTRICT_TOTAL_SECOND: # 如果第一次访问距现在已经有 RESTRICT_TOTAL_SECOND 时间了
                        ret.start_time = now
                        ret.count = 1
                    elif ret.count > RESTRICT_COUNT:
                        ret.is_lock = True
                        ret.start_time = now
                        ret.save()
                        return HttpResponse('操作过于频繁，十分钟后再试', status=403)

                    ret.save()
                    if during_sec < SECOND_INTERVAL: # 如果操作频繁，小于最少间隔时间
                        return HttpResponse('操作过于频繁，请 %d 秒后再试' % SECOND_INTERVAL, status=403)
