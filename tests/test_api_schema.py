from fibery.client.schema import FiberySchema


def test_get(setup, fibery, requests_mock):
    requests_mock.post(
        "https://foobar.fibery.io/api/commands",
        text="""[
  {
    "success": true,
    "result": {
      "fibery/id": "fd5d9550-3779-11e9-9162-04d77e8d50cb",
      "fibery/types": [
        {
          "fibery/name": "software-development/user-story",
          "fibery/fields": [
            {
              "fibery/name": "fibery/modification-date",
              "fibery/type": "fibery/date-time",
              "fibery/meta": {
                "fibery/modification-date?": true,
                "fibery/readonly?": true,
                "fibery/default-value": "$now",
                "fibery/secured?": false,
                "fibery/required?": true,
                "ui/object-editor-order": 8
              },
              "fibery/id": "e36a91b1-3f4b-11e9-8051-8fb5f642f8a5"
            },
            {
              "fibery/name": "assignments/assignees",
              "fibery/type": "fibery/user",
              "fibery/meta": {
                "fibery/collection?": true,
                "ui/object-editor-order": 4,
                "fibery/relation": "c3e75ca4-8d15-11e9-b98a-9abbdf4720ab"
              },
              "fibery/id": "2cd92374-3839-11e9-9162-04d77e8d50cb"
            }
          ],
          "fibery/meta": {
            "fibery/primitive?": false,
            "fibery/domain?": true,
            "ui/color": "#068cba",
            "app/mixins": {
              "fibery/rank-mixin": true,
              "assignments/assignments-mixin": true,
              "Files/Files-mixin": true,
              "workflow/workflow": true,
              "comments/comments-mixin": true
            },
            "fibery/secured?": true
          },
          "fibery/id": "2c4213ae-3839-11e9-9162-04d77e8d50cb"
        }
      ],
      "fibery/meta": {
        "fibery/version": "1.0.62",
        "fibery/rel-version": "1.0.6",
        "fibery/maintenance?": false,
        "maintenance?": false
      }
    }
  }
]""",
    )

    schema: FiberySchema = fibery.schema.get()

    assert schema.id == "fd5d9550-3779-11e9-9162-04d77e8d50cb"
    assert len(schema.types) == 1
    assert isinstance(schema.meta, dict)

    schema_type = schema.types[0]
    assert schema_type.id == "2c4213ae-3839-11e9-9162-04d77e8d50cb"
    assert len(schema_type.fields) == 2
