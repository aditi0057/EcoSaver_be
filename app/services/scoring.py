def calclulate_ecoscore(product: dict) -> dict:
    score = 0
    breakdown= {}

    #sustainability factor(30%)
    factor = str(product.get('sustainability_factors', '')).lower()
    if 'biodegradable' in factor:
        breakdown['sustainability'] = 30
    elif 'reusable' in factor:
        breakdown['sustainability'] = 25
    elif 'natural' in factor:
        breakdown['sustainability'] = 20
    else:
        breakdown['sustainability'] = 10

    score += breakdown['sustainability']

    #certfications(20%)
    certs = str(product.get('certification_tags', '')).split(',')
    cert_score = 0
    for cert in certs:
        cert = cert.strip()
        if cert in ['USDA Certified Biobased', 'FSC Certified', 'ECOCERT','GOTS CERTIFIED','USDA Organic','Ayurveda Mark']:
            cert_score+=5
        elif cert in ['OK Compost','BPA-free']:
            cert_score+=3
    breakdown['certifications'] = min(20,cert_score)
    score += breakdown['certifications']

    #End of Life Disposal(20%)
    disposal = str(product.get('end_of_life_disposal','')).lower()
    if 'compost' in disposal:
        breakdown['disposal'] = 20
    elif 'recycle' in disposal:
        breakdown['disposal'] = 15
    elif 'landfill' in disposal:
        breakdown['disposal'] = 5
    else:
        breakdown['disposal'] = 10 #fallback

    score += breakdown['disposal']

    #packagin material(15%)
    material = str(product.get('product_description', '') + ' ' + product.get('product_name','')).lower()
    if any(x in material for x in ['bamboo','cotton','wood']):
        breakdown['product_material'] = 15
    elif any(x in material for x in ['glass', 'metal']):
        breakdown['product_material'] = 12
    elif any(x in material for x in ['biodegradable', 'compostable']):
        breakdown['product_material'] = 10
    else:
        breakdown['product_material'] = 5
    score += breakdown['product_material']

    #Bonus for sustainability flag
    if product.get('is_sustainable'):
        score = min(100, score+5)
        breakdown['bonus_sustainability_flag'] = 5
    else:
        breakdown['bonus_sustainability_flag'] = 0

    return {
        "eco_score": min(100,score),
        "breakdown": breakdown
    }
