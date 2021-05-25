def test_create(setup, fibery, requests_mock):
    requests_mock.get(
        "https://foobar.fibery.io/api/webhooks/v2",
        text="""[
  {
    "id": 5,
    "url": "http://webhook.site/c2d6d113-aebe-4f68-a337-022ec3c7ab5d",
    "type": "Cricket/Player",
    "state": "active",
    "runs": [
      {
        "http_status": "200",
        "elapsed_time": "209",
        "request_time": "2019-07-30T07:18:49.883Z"
      },
      {
        "http_status": "200",
        "elapsed_time": "181",
        "request_time": "2019-07-30T07:23:06.738Z"
      }
    ]
  }
]""",
    )

    result = fibery.webhook.list()

    assert len(result) == 1

    webhook = result[0]

    assert webhook.id == 5

    assert webhook.url == "http://webhook.site/c2d6d113-aebe-4f68-a337-022ec3c7ab5d"
    assert webhook.state == "active"
    assert webhook.type == "Cricket/Player"
    assert len(webhook.runs) == 2
    assert webhook.runs[0].http_status == "200"
