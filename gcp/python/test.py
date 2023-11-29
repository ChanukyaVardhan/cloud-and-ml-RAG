import sys
sys.path.append('generated/')

import grpc
import text_embedding_pb2
import text_embedding_pb2_grpc

def run():
    # with grpc.insecure_channel('localhost:50051') as channel:
    with grpc.insecure_channel('34.74.89.40:80') as channel:
        stub = text_embedding_pb2_grpc.TextEmbeddingStub(channel)
        # response = stub.SaveTextEmbedding(text_embedding_pb2.SaveTextEmbeddingRequest(
        #     url="https://seekingalpha.com/article/4654739-finding-fee-savings-in-fixed-income",
        #     text="Summary As indexing has grown, investors have benefited substantially by saving on fees and avoiding active underperformance. These benefits are not limited just to equities but have also extended to other asset classes including the fixed income space. Index bond fund expenses in the U.S. and Europe have been consistently lower than their active counterparts for the past decade. One of the benefits of indexing is its low cost relative to active management. As indexing has grown, investors have benefited substantially by saving on fees and avoiding active underperformance. These benefits are not limited just to equities but have also extended to other asset classes including the fixed income space, where fees can play a particularly pivotal role. In Exhibit 1, we see that index bond fund expenses in the U.S. and Europe have been consistently lower than their active counterparts for the past decade. While that spread has narrowed in recent years, we still observe a fee differential of 39 bps in the U.S. and 55 bps in Europe as of 2022. Using the same average fee differentials between active and passive fixed income funds in the U.S. and Europe, as applied regionally to approximately USD 102 billion of assets invested in mutual funds and ETFs tracking iBoxx corporate bond indices in both regions, we can estimate a current run rate of equal to at least USD 465 million per year in fee savings made by passive investors thanks in part to the iBoxx series (see Exhibit 2). Of course, this USD 465 million estimate understates the full cost savings of the fixed income index industry, since it encompasses funds tracking only select indices from S&P Dow Jones Indices in the U.S. and Europe. Our Annual Survey of Indexed Assets shows global assets tracking our iBoxx Corporate indices were USD 121 billion as of December 2022 (this also includes institutional segregated mandates, as well as assets outside the U.S. and Europe). To provide context on the size of the passive market in fixed income, this number makes up only 1% of the global total of USD 11.5 trillion in assets of all open-end bond funds 1and only around 0.5% of global rated corporate debt outstanding. In other words, there is plenty of headroom for future passive growth in fixed income, and the prospects for greater fee savings are promising. Obviously, the savings generated by the shift from active to passive management would be of no consolation if investors lost more in performance shortfalls than they gained in reduced fees. As readers of our SPIVA®reports may know, in the 15 years ending in June 2023, 94% of allactively managedGeneral Investment Grade bond funds lagged the iBoxx $ Liquid Investment Grade Index. High Yield results were almost equally disappointing. As indexing in fixed income has gained momentum, bond market participants have benefited from fee savings and avoidance of active underperformance, a powerful combination. Regulated open-end funds include mutual funds, exchange-traded funds (ETFs) and institutional funds. Level of global rated corporate debt reached USD 23.2 trillion as of July 1, 2023.")
        # )

        response = stub.SaveTextEmbedding(text_embedding_pb2.SaveTextEmbeddingRequest(
            url="https://seekingalpha.com/article/4654904-air-france-klm-dodges-shocking-aviation-war-with-the-us",
            text="Summary Air France-KLM has achieved more unity and stronger decision-making under new CEO Benjamin Smith but faced pressures from the government. The Dutch government's plan to reduce flight movements at Amsterdam Schiphol Airport faced international backlash and has been abandoned.The reduced risk and political support may allow Air France-KLM to pursue growth opportunities and bolster its M&A activity. Looking for more investing ideas like this one? Get them exclusively at The Aerospace Forum. Learn More »JanJBrand/iStock Unreleased via Getty ImagesAir France-KLM (OTCPK:AFLYY,OTCPK:AFRAF) is a company that for a long time has struggled with itself. The combination of the French and Dutch carrier painfully showed how cultural and labor differences led to acarrier underperforming with significant distrust in all layers of the company between the French and Dutch part of the business. With the departure of Pieter Elbers as CEO of KLM and the arrival of Benjamin Smith as CEO of the airline group, it finally seems that there is some peace in the house with the company making more unified decisions and seemingly is getting out of the crushing pandemic as a stronger company.However, in The Netherlands we have been seeing support for air travel crumble as there is a big climate agenda. Despite the big projection of economic growth enabled by KLM'shub Amsterdam Schiphol Airport, there have beenstudies(news report in Dutch) suggesting that the contribution of Schiphol to the Dutch economy is minor. From there, no longer limiting the number of flights executed annually was not something that many politicians felt could be defended with climate change also playing a role. However, as I discuss in this report, this almost had negative consequences that would reach further than anticipated.Government Forces Schiphol To Shrink18rosemary36lennard.comThe number of airplane movements for Schiphol has been capped on 500,000 per year, but due to Schiphol exceeding noise regulations, the government wanted to force a reduction of 8% to 460,000 airplane movements. The fact that studies suggested the marginal impact on the Dutch economy did not help Schiphol or KLM's case to keep the number of airplane movements at 500,000. Having read some commentary and reports, advocates of a cut suggested that transfer passengers are not adding anything to the Dutch economy while just removing those passengers and associated flights would provide a significant reduction in flight movements against little loss to the economy.I majored in aerospace engineering and what is clear to me is that this line of reasoning has been short-sighted at best as it assumed a modular setting where removing one block would not lead to a collapse of an entire system. Putting it simple, removing transfer passengers would possibly not directly inflict damage to the economy but the indirect damages would certainly be there as the hub function which feeds value adding traffic to and from The Netherlands would come under pressure. The reduction of the transfer function for Schiphol would have consequences for its appeal as a hub and would cause harm to tourism and the business climate and provide a cascading economic damage as well as reductions to innovation. Besides that, aviation and politics are intertwined and the Dutch economy could be on the losing end if that overlooked connection would start hitting back Dutch businesses.The Politics Of International Aviation Steam Rolls Shrink PlanIn a reportpublishedin August this year, I pointed out that Air France-KLM was facing some pressure due to prospective flight caps at Schiphol Airport. KLM along with other parties took the Dutch State to court over the reduction of flight movements from 500,000 to 460,000 and initially won only to see the government successfully appealing. What the government and likely not even KLM had expected was that the reduction of flight movements would become an international issue that almost caused an aviation war between the US and The Netherlands.18rosemary36lennard.comHow can this happen? As part of the reduction in flight movements that was set to take effect in April 2024, new airlines operating on Schiphol would lose their slots. Among those airlines were JetBlue (JBLU) and Air India while Delta Air Lines (DAL) was also facing a reduction in slot allocations. In total, American carriers were set to lose 1,135 slots. The US Department of Transport declared the complaint regarding slot reductions at Schiphol as admissible and it set in motion negotiations between the Dutch authorities and Brussels. The possibility of retaliation was real as Dutch airlines of which KLM is the most prominent one had to submit schedules, which could have become the starting sign of a retaliation that would see KLM's US business reduce by more than 20%.What the Dutch government quickly found out is that while studies suggest the economic damage of a smaller Schiphol Airport are manageable, the connection between aviation and politics that was not accounted for would lead to substantial economic harm to Dutch businesses directly and indirectly and a loss of face in the geopolitical landscape. The Dutch government put its own flag carrier in the crosshairs of its own plan as well as the crosshairs of any retaliation.A Well Thought Out Plan For The Bin: KLM Comes Out As A WinnerThe noise reduction plan that would mandate a flight movement reduction had never been a strong one as it in my view insufficiently accounted for noise reduction by means of utilizing airplanes with lover noise emissions and it did assume that instead of an 8% reduction in slot allocation for all operators, new operators would automatically lose slots. There is no proper justification for applying the rule in such a disproportionate way and perhaps it was in KLM's luck that Schiphol filled in the noise reduction plan as such, as it directly sparked involvement of the US and European Commission, which resulted in the slot reduction plan to be abandoned.Conclusion: Risk Has Reduced Somewhat For Air France-KLMWith the proposed reductions in slots off the table, I think the risk has somewhat reduced for KLM in particular. However, I do believe that some uncertainty regarding any capacity reduction plans persists. The company could possibly count on some political support as the winner of the recently-held Dutch elections is not a proponent of pressuring airlines for the sake of emissions and noise reduction. Furthermore, on group level I believe that Air France-KLM could have some additional movement space to grow in the years to come if the flight cap is not lowered from the current level of 500,000, and apart from that I do believe that the current stance of the Dutch government also makes the company more eager to bolster its M&A activity asseenrecently while upgauging of airplanes will provide more efficient growth opportunity ahead.With a reduced ceiling for flight movements off the table as well as the possibility for any retaliation, I believe that the risks for Air France-KLM have somewhat reduced and maintain my buy rating for the stock.Editor's Note: This article discusses one or more securities that do not trade on a major U.S. exchange. Please be aware of the risks associated with these stocks.If you want full access to all our reports, data and investing ideas,join The Aerospace Forum, the #1 aerospace, defense and airline investment research service on Seeking Alpha, with access to evoX Data Analytics, our in-house developed data analytics platform.This article was written byDhierin Bechai15.46KFollowersFollowDhierin-Perkash Bechai is an aerospace, defense and airline analyst.Dhierin runs the investing groupThe Aerospace Forum, whose goal is to discover investment opportunities in the aerospace, defense and airline industry. With a background in aerospace engineering, he provides analysis of a complex industry with significant growth prospects, and offers context to developments as they occur, describing how they might affect investment theses. His investing ideas are driven by data informed analysis. The investing group also provides direct access to data analytics monitors.Learn more.Analyst’s Disclosure:I/we have no stock, option or similar derivative position in any of the companies mentioned, and no plans to initiate any such positions within the next 72 hours.I wrote this article myself, and it expresses my own opinions. I am not receiving compensation for it (other than from Seeking Alpha). I have no business relationship with any company whose stock is mentioned in this article.")
        )
        print("Server response: ", response.status)

if __name__ == '__main__':
    run()