from src.agents.agents import build_search_agent , build_Reader_agent , writer_agent , critic_agent


def run_search_pipeline(topic : str) -> dict :

    state = {}

    print("\n" + "="*50)
    print("step 1 - research agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user" , f"Find recent , reliable and detailed information about {topic}")]
    })

    state['search_result'] = search_result['messages'][-1].content

    print("\n search result : " ,state['search_result'] )



    print("\n" + "="*50)
    print("step 2 - reader agent is working ...")
    print("="*50)

    reader_agent = build_Reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages" : [(
                'user' , 
                  f"Based on the following search results about {topic}"
                  f"pick the most relevant URL and scrape it for deeper content.\n\n"
                  f"Search results : \n {state['search_result']}"      
            )
                
            ]
        }
    )
    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n scraped content : \n" , state['scraped_content'])

    print("\n" + "="*50)
    print("step 3 - writer agent is working ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state['report'] = writer_agent.invoke(
        {
            "topic" : topic ,
            "research" : research_combined 
        }
    )


    print("\n Final report :\n" , state["report"])


    print("\n" + "="*50)
    print("step 4 - critic agent is working ...")
    print("="*50)

    state['score'] = critic_agent.invoke(
        {
            "report" : state['report']
        }
    )

    print("\n Final Score :" , state['score'])

    return state
