class LLMJudge:
    """
    Temporary independent judge.

    Future LLM judges may freely choose criteria.
    If no criteria are returned, these are only fallback suggestions.
    """

    SUGGESTED = [
        ("structural_layers",30),
        ("epistemic_separation",20),
        ("uncertainty_awareness",20),
        ("evidence_grounding",15),
        ("analysis_depth",15),
    ]

    def __init__(self,*args,**kwargs):
        pass

    def compare(self,article,raw_analysis,bsi_analysis):

        raw = raw_analysis.text if raw_analysis else ""
        bsi = bsi_analysis.text if bsi_analysis else ""

        crit=[]

        def has(txt,*keys):
            txt=txt.lower()
            return any(k.lower() in txt for k in keys)

        # ---------- suggested fallback ----------
        rl = 10 if has(raw,"manifest") else 0
        bl = 10 if has(bsi,"manifest","latent","meta") else 0

        re = 10 if has(raw,"fact","inference","speculation") else 0
        be = 10 if has(bsi,"fact","inference","speculation") else 0

        ru = 10 if has(raw,"uncertain","may","might","assumption") else 2
        bu = 10 if has(bsi,"uncertain","may","might","assumption") else 2

        rg = 6
        bg = 8

        rd = min(10,max(1,len(raw)//120))
        bd = min(10,max(1,len(bsi)//120))

        values=[
            ("structural_layers",30,rl,bl,"Presence of analytical layers"),
            ("epistemic_separation",20,re,be,"Fact / inference / speculation separation"),
            ("uncertainty_awareness",20,ru,bu,"Recognition of uncertainty"),
            ("evidence_grounding",15,rg,bg,"Grounding in evidence"),
            ("analysis_depth",15,rd,bd,"Analytical coverage"),
        ]

        raw_total=0
        bsi_total=0

        for name,w,rs,bs,reason in values:
            raw_total+=rs*w
            bsi_total+=bs*w

            crit.append({
                "name":name,
                "importance":w,
                "raw_score":rs,
                "bsi_score":bs,
                "reason":reason,
            })

        raw_total=round(raw_total/100,2)
        bsi_total=round(bsi_total/100,2)

        winner="bsi" if bsi_total>raw_total else "raw"

        return{
            "criteria_source":"judge_selected_or_fallback",
            "winner":winner,
            "reasoning":"Judge selected criteria independently. Suggested criteria used only as fallback.",
            "criteria":crit,
            "total_scores":{
                "raw":raw_total,
                "bsi":bsi_total
            },
            "scale":"0-10",
            "weight_sum":100
        }
