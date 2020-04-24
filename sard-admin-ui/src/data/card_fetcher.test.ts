import { listProcessingCore } from './card_fetcher'


describe('Card fetcher', () => {
    it('returns a list of evidences', async () => {
        const resp  = new Response(`
        {
            "data": {
              "board": {
                "list": {
                  "cards": [
                    {
                      "title": "M190428",
                      "archived": false
                    },
                    {
                      "title": "M190429",
                      "archived": false
                    }
                  ]
                }
              }
            }
          }
        `)
        const result = await listProcessingCore(resp)
        expect(result).toHaveLength(2)
    })
    it('should have id, path, and status', async () => {
        const resp  = new Response(`
        {
            "data": {
              "board": {
                "list": {
                  "cards": [
                    {
                      "title": "M190428",
                      "archived": false,
                      "customFields": [
                        {
                          "customField": {
                            "name": "auto"
                          },
                          "value": "190074"
                        },
                        {
                          "customField": {
                            "name": "ipl"
                          },
                          "value": "ipl_190152_PFO"
                        },
                        {
                          "customField": {
                            "name": "item"
                          },
                          "value": "01"
                        },
                        {
                          "customField": {
                            "name": "path"
                          },
                          "value": "/operacoes/ipl_190152_PFO/auto_apreensao_190074/M190428/M190428.dd"
                        },
                        {
                          "customField": {
                            "name": "profile"
                          },
                          "value": "fastrobust"
                        },
                        {
                          "customField": {
                            "name": "registro"
                          },
                          "value": null
                        },
                        {
                          "customField": {
                            "name": "status"
                          },
                          "value": "done"
                        }
                      ]
                    }
                  ]
                }
              }
            }
          }
        `)
        const result = await listProcessingCore(resp)
        expect(result).toHaveLength(1)
        const x0 = result[0]
        expect(x0).toHaveProperty('id')
        expect(x0).toHaveProperty('properties')
        expect(x0.id).toEqual("M190428")
        expect(x0.properties).toEqual({
            auto: "190074",
            ipl: "ipl_190152_PFO",
            item: "01",
            path: "/operacoes/ipl_190152_PFO/auto_apreensao_190074/M190428/M190428.dd",
            profile: "fastrobust",
            registro: "",
            status: "done",
        })
    })
})

