const listProcessingQuery = `
{
    board(title: "Materiais") {
      list(title: "Processamento") {
        cards {
          title
          archived
          customFields {
            customField {
              name
            }
            value
          }
        }
      }
    }
  }
`
export type CardFetcherType = {
    listProcessing: () => Promise<ProcessingCard[]>
}

export function CardFetcher({ graphqlURL }: { graphqlURL: string }): CardFetcherType {
    return {
        listProcessing: async () => {
            const req = new Request(graphqlURL, {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: listProcessingQuery }),
            })
            const resp = await fetch(req)
            return listProcessingCore(resp)
        }
    }
}

export type ProcessingCard = {
    id: string,
    properties: {
        auto?: string,
        ipl?: string,
        item?: string,
        path?: string,
        profile?: string,
        registro?: string,
        status?: string,
    },
}

export async function listProcessingCore(resp: Response): Promise<ProcessingCard[]> {
    if (!resp.ok) {
        const text = await resp.text()
        throw new Error(text)
    }
    const j = await resp.json()
    const { cards } = j.data.board.list
    const result = cards.map((x: any) => {
        const p: ProcessingCard = {
            id: x.title,
            properties: {},
        }
        if (x.customFields) {
            x.customFields.forEach((c: {
                customField: {
                    name: keyof ProcessingCard["properties"]
                },
                value: string,
            }) => {
                p.properties[c.customField.name] = (c.value == null) ? "" : c.value
            });
        }
        return p
    })
    return result
}

export function MockCardFetcher(): CardFetcherType {
    return {
        listProcessing: async () => {
            const x: ProcessingCard[] = [
                {
                    id: "M190001", properties: {
                        auto: "",
                        ipl: "ipl_180001",
                        item: "1",
                        path: "/operacoes/ipl_180001/item01-M190001/item01-M190001.dd",
                        profile: "",
                        registro: "R190020",
                        status: "done",
                    }
                },
                {
                    id: "M190002", properties: {
                        auto: "",
                        ipl: "ipl_180001",
                        item: "1",
                        path: "/operacoes/ipl_180001/item01-M190002/item01-M190002.dd",
                        profile: "",
                        registro: "R190020",
                        status: "done",
                    }
                },
                {
                    id: "M190003", properties: {
                        auto: "",
                        ipl: "ipl_180001",
                        item: "1",
                        path: "/operacoes/ipl_180001/item01-M190003/item01-M190003.dd",
                        profile: "",
                        registro: "R190020",
                        status: "failed",
                    }
                },
                {
                    id: "M190004", properties: {
                        auto: "",
                        ipl: "ipl_180001",
                        item: "1",
                        path: "/operacoes/ipl_180001/item01-M190004/item01-M190004.dd",
                        profile: "",
                        registro: "R190020",
                        status: "",
                    }
                },
                {
                    id: "M190005", properties: {
                        auto: "",
                        ipl: "ipl_180001",
                        item: "1",
                        path: "/operacoes/ipl_180001/item01-M190005/item01-M190005.dd",
                        profile: "",
                        registro: "R190020",
                        status: "running",
                    }
                },
                {
                    id: "M190006", properties: {
                        auto: "",
                        ipl: "ipl_180001",
                        item: "1",
                        path: "/operacoes/ipl_180001/item01-M190006/item01-M190006.dd",
                        profile: "",
                        registro: "R190020",
                        status: "running",
                    }
                },
            ]
            return x
        }
    }
}
