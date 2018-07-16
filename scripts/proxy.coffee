proxy = require 'proxy-agent'
module.exports = (robot) ->
  robot.globalHttpOptions.httpAgent  = proxy('http://1w1305198:Takuya123@www-proxy.waseda.jp:8080', false)
  robot.globalHttpOptions.httpsAgent = proxy('http://1w1305198:Takuya123@www-proxy.waseda.jp:8080', true)