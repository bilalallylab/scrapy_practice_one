from rotating_proxies.policy import BanDetectionPolicy


class PolicyOne(BanDetectionPolicy):
    def response_is_ban(self, request, response):
        ban = super(PolicyOne, self).response_is_ban(request, response)
        return ban

    def exception_is_ban(self, request, exception):
        # override method completely: don't take exceptions in account
        return None
