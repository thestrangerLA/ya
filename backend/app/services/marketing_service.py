"""
AI Marketing Engine Service — Generates responsible, database-backed marketing materials.
Never invents false claims or misleading medical statements.
"""

from typing import List, Dict, Any
from app.models.models import Medicine


class AIMarketingService:

    @staticmethod
    def generate_marketing_copy(medicine: Medicine, tone: str = "Professional", target_audience: str = "เกษตรกรและคนเลี้ยงสัตว์") -> Dict[str, Any]:
        med_name = medicine.name
        brand = medicine.brand or "แบรนด์คุณภาพ"
        animal = medicine.animal_type.name if medicine.animal_type else "สัตว์เลี้ยงและปศุสัตว์"
        animal_icon = medicine.animal_type.icon if medicine.animal_type else "🐾"
        category = medicine.category.name if medicine.category else "เวชภัณฑ์สัตว์"
        indications = medicine.indications or "ช่วยดูแลสุขภาพและรักษาอาการป่วยตามมาตรฐานสัตวแพทย์"
        dosage = medicine.dosage or "ควรใช้ตามขนาดและคำแนะนำบนฉลาก"
        warnings = medicine.warnings or "อ่านคำเตือนและระยะหยุดยาก่อนใช้"
        price_str = f"฿{medicine.price:,.2f}" if medicine.price else "สอบถามราคาหน้าร้าน"

        # Tone modifiers
        tone_intro = {
            "Professional": f"ขอแนะนำ {med_name} เวชภัณฑ์มาตรฐานระดับสัตวแพทย์ เพื่อสุขภาพที่ดีของ{animal}",
            "Friendly": f"ดูแล{animal_icon} {animal} ตัวโปรดของคุณด้วย {med_name} จาก {brand} สุขภาพดี อารมณ์ดีทุกวัน!",
            "Funny": f"บอกลาปัญหาป่วยๆ ของ{animal}! ให้ {med_name} ช่วยแล แล้วคุณจะยิ้มได้ ร่างกาย{animal}จะฟิตปั๋ง!",
            "Emotional": f"เพราะ{animal} คือสมาชิกคนสำคัญในครอบครัว เลือก {med_name} ปกป้องเขาอย่างเต็มที่ด้วยความรัก",
            "Urgency": f"🚨 อย่าปล่อยให้อาการป่วยบานปลาย! ปกป้อง {animal} ของคุณวันนี้ด้วย {med_name} ก่อนสายเกินไป!",
            "Luxury": f"ที่สุดแห่งการดูแลระดับพรีเมียม {med_name} เวชภัณฑ์ทรงประสิทธิภาพจาก {brand} สำหรับ {animal}",
            "Educational": f"💡 สาระน่ารู้การดูแล {animal}: ข้อบ่งใช้และประสิทธิภาพของ {med_name} ที่ผู้เลี้ยงควรรู้",
            "Storytelling": f"จากประสบการณ์การดูแล {animal} ให้แข็งแรง สมบูรณ์ เคล็ดลับสำคัญอยู่ที่การเลือกใช้ {med_name}",
        }.get(tone, f"ขอแนะนำ {med_name} สำหรับ {animal}")

        hook = f"🔥 {med_name} ตัวช่วยดูแล {animal} ที่ตอบโจทย์การรักษาและปกป้องอย่างตรงจุด!"
        headline = f"ปกป้อง {animal} ของคุณให้แข็งแรงปลอดภัย ด้วย {med_name}"
        customer_benefit = f"ช่วยรักษาอาการป่วยและฟื้นฟูสุขภาพของ {animal} ได้อย่างมีประสิทธิภาพ ปลอดภัยตามคำแนะนำการใช้ยา"
        
        fb_post = f"""{tone_intro}

{hook}

📋 **ข้อบ่งใช้และสรรพคุณ:**
{indications}

💉 **ขนาดและวิธีการใช้:**
{dosage}

⚠️ **ข้อระวังและระยะหยุดยา:**
{warnings}

🏷️ **หมวดหมู่:** {category} | **แบรนด์:** {brand}
💰 **ราคา:** {price_str}

สนใจสั่งซื้อหรือสอบถามข้อมูลเพิ่มเติม ทักแชทหาเราได้ทันทีครับ! 💚
#ยาสัตว์ #{brand.replace(' ', '')} #ดูแล{animal.replace(' ', '')} #เวชภัณฑ์สัตว์"""

        short_caption = f"{med_name} — ตัวช่วยดูแล {animal} ให้แข็งแรง ปลอดภัยตามมาตรฐาน 💊 สั่งซื้อได้แล้ววันนี้!"
        long_caption = f"{tone_intro}\n\nสรรพคุณ: {indications[:150]}...\nใช้สำหรับ {animal} ปริมาณแนะนำ: {dosage[:100]}...\nคำเตือน: {warnings[:100]}..."
        promotional_text = f"🎉 โปรโมชั่นพิเศษ! {med_name} สินค้าคุณภาพสำหรับ {animal} ราคาเพียง {price_str} ของแท้ 100% สั่งเลย!"
        product_description = f"{med_name} โดย {brand} เป็นเวชภัณฑ์ในกลุ่ม {category} ออกแบบมาสำหรับ {animal} โดยเฉพาะ สรรพคุณ: {indications}"
        call_to_action = f"📲 สั่งซื้อ {med_name} หน้าร้านหรือทักแชทปรึกษาเพิ่มเติมได้เลยครับ!"
        
        bullet_points = [
            f"ตรงเข้าจัดการปัญหา: {indications[:80]}...",
            f"เหมาะสำหรับ: {animal}",
            f"ใช้ง่าย กำหนดขนาดชัดเจน: {dosage[:60]}...",
            f"ปลอดภัยสูงเมื่อใช้ตามคำเตือน: {warnings[:60]}...",
            f"ราคาคุ้มค่า: {price_str}"
        ]

        faq = [
            {"question": f"{med_name} เหมาะกับสัตว์ประเภทไหน?", "answer": f"เหมาะสำหรับ {animal} โดยเฉพาะ"},
            {"question": f"มีข้อระวังอะไรในการใช้ยาไหม?", "answer": warnings},
            {"question": f"ใช้อย่างไรและปริมาณเท่าไหร่?", "answer": dosage},
        ]

        return {
            "facebook_post": fb_post,
            "short_caption": short_caption,
            "long_caption": long_caption,
            "promotional_text": promotional_text,
            "product_description": product_description,
            "call_to_action": call_to_action,
            "headline": headline,
            "hook": hook,
            "customer_benefit": customer_benefit,
            "bullet_points": bullet_points,
            "faq": faq,
        }

    @staticmethod
    def generate_campaign(medicine: Medicine, campaign_type: str) -> Dict[str, Any]:
        med_name = medicine.name
        animal = medicine.animal_type.name if medicine.animal_type else "ปศุสัตว์และสัตว์เลี้ยง"
        price_str = f"฿{medicine.price:,.2f}" if medicine.price else "ราคาสุดคุ้ม"

        campaign_data = {
            "Flash Sale": {
                "title": f"⚡ FLASH SALE 24 ชม.! ลดราคาพิเศษ {med_name}",
                "headline": f"ด่วน! {med_name} สำหรับ {animal} ราคาพิเศษจำนวนจำกัด",
                "discount": "ส่วนลดพิเศษสูงสุด 15% หน้าร้าน",
                "cta": "🛒 สั่งซื้อด่วนก่อนสินค้าหมดสต็อก!",
            },
            "New Product": {
                "title": f"✨ เปิดตัวเวชภัณฑ์ใหม่! {med_name}",
                "headline": f"นวัตกรรมการดูแล {animal} ตัวใหม่ล่าสุด {med_name}",
                "discount": "รับส่วนลด 10% สำหรับสั่งซื้อครั้งแรก",
                "cta": "📲 สัมผัสประสิทธิภาพใหม่ สั่งซื้อได้ก่อนใคร!",
            },
            "Holiday Promotion": {
                "title": f"🎁 โปรโมชั่นต้อนรับเทศกาลต้อนรับสุขภาพดี {animal}",
                "headline": f"มอบสุขภาพที่ดีเป็นของขวัญให้ {animal} ด้วย {med_name}",
                "discount": "ซื้อครบ 1,000 บาท แลกซื้อราคาพิเศษ",
                "cta": "🛍️ สั่งซื้อของขวัญสุขภาพให้สัตว์เลี้ยงวันนี้!",
            },
            "Bundle Promotion": {
                "title": f"📦 ชุดเซ็ตประหยัดสุดคุ้ม! {med_name} + อุปกรณ์ดูแล",
                "headline": f"จับคู่ดูแล {animal} ครบเซ็ต ปลอดภัย คุ้มค่ากว่าเดิม",
                "discount": "ประหยัดกว่าซื้อแยกชิ้นถึง 20%",
                "cta": "📦 เลือกซื้อชุดเซ็ตสุดคุ้มเลย!",
            },
            "Seasonal Promotion": {
                "title": f"🌧️ โปรโมชั่นรับฤดูกาล ดูแล {animal} ปลอดโรค",
                "headline": f"เตรียมพร้อมรับมือฤดูกาลใหม่ ปกป้อง {animal} ด้วย {med_name}",
                "discount": "ส่วนลดพิเศษต้อนรับฤดูกาล",
                "cta": "🛡️ ป้องกันก่อนป่วย สั่งซื้อวันนี้!",
            },
            "Free Shipping": {
                "title": f"🚚 จัดส่งฟรีทั่วประเทศ! เมื่อสั่งซื้อ {med_name}",
                "headline": f"ส่งตรงถึงฟาร์มและบ้านคุณ ฟรีค่าจัดส่ง {med_name}",
                "discount": "ฟรีค่าจัดส่งทุกออเดอร์ไม่มีขั้นต่ำ",
                "cta": "🚚 กดสั่งซื้อเพื่อรับสิทธิ์ส่งฟรีทันที!",
            },
            "Discount": {
                "title": f"🏷️ โปรโมชั่นลดราคาสุดพิเศษ {med_name}",
                "headline": f"เวชภัณฑ์คุณภาพสำหรับ {animal} ในราคาประหยัดสบายกระเป๋า",
                "discount": f"ราคาพิเศษเพียง {price_str}",
                "cta": "👉 คลิกสั่งซื้อรับส่วนลดทันที!",
            },
            "Limited Time": {
                "title": f"⏳ ข้อเสนอมีเวลาจำกัด! {med_name} ราคาพิเศษ",
                "headline": f"เหลือเวลาอีกไม่นาน! เป็นเจ้าของ {med_name} ในราคาที่ดีที่สุด",
                "discount": "ข้อเสนอราคาสุดพิเศษภายในสัปดาห์นี้เท่านั้น",
                "cta": "⏰ อย่ารอช้า สั่งซื้อด่วน!",
            },
            "Buy One Get One": {
                "title": f"🎉 ซื้อ 1 แถม 1! โปรโมชั่นสุดตระการตา {med_name}",
                "headline": f"คุ้มที่สุดในรอบปี ซื้อ {med_name} รับของแถมดูแลสุขภาพสัตว์ฟรี",
                "discount": "ซื้อ 1 ชิ้น แถมฟรี 1 ชิ้น",
                "cta": "🎁 รับสิทธิ์โปรซื้อ 1 แถม 1 ทันที!",
            },
        }.get(campaign_type, {
            "title": f"🎉 แคมเปญพิเศษ {med_name}",
            "headline": f"ข้อเสนอพิเศษสำหรับ {animal}",
            "discount": "ส่วนลดคุ้มค่า",
            "cta": "สั่งซื้อเลย!",
        })

        caption = f"""{campaign_data['title']}

{campaign_data['headline']}

✨ **สิทธิประโยชน์แคมเปญ:**
• {campaign_data['discount']}
• เวชภัณฑ์ยา {med_name} ของแท้ 100% สำหรับ {animal}
• สรรพคุณ: {medicine.indications or 'ดูแลสุขภาพและรักษาอาการป่วย'}

{campaign_data['cta']} หน้าร้านหรือทักแชทสอบถามเลยครับ!"""

        return {
            "campaign_title": campaign_data["title"],
            "campaign_type": campaign_type,
            "target_audience": f"ผู้เลี้ยง {animal} และเจ้าของฟาร์ม",
            "key_selling_point": f"เวชภัณฑ์คุณภาพ {med_name} ช่วยดูแลรักษา {animal} อย่างปลอดภัย",
            "promotional_headline": campaign_data["headline"],
            "post_caption": caption,
            "discount_structure": campaign_data["discount"],
            "call_to_action": campaign_data["cta"],
            "terms_and_conditions": "เงื่อนไขเป็นไปตามที่ร้านกำหนด สินค้ามีจำนวนจำกัด โปรดอ่านคำเตือนก่อนใช้ยา",
        }

    @staticmethod
    def generate_image_prompts(medicine: Medicine, color_theme: str, marketing_goal: str) -> Dict[str, Any]:
        med_name = medicine.name
        animal = medicine.animal_type.name if medicine.animal_type else "livestock"
        indications = medicine.indications or "veterinary health"

        base_prompt = (
            f"Commercial advertisement photography for veterinary medicine '{med_name}', "
            f"featuring clean product bottle packaging in center focus with {color_theme} color palette, "
            f"healthy and active {animal} in clean modern farm background, soft dramatic lighting, "
            f"cinematic composition, high detail, 8k resolution, ultra realistic, professional product design"
        )

        return {
            "medicine_name": med_name,
            "animal_type": animal,
            "color_theme": color_theme,
            "square_prompt": f"{base_prompt}, 1:1 aspect ratio, centered square layout for Instagram post",
            "portrait_prompt": f"{base_prompt}, 9:16 aspect ratio, vertical story poster layout for TikTok and IG Story",
            "landscape_prompt": f"{base_prompt}, 16:9 aspect ratio, wide hero banner layout for Facebook cover and Website header",
        }

    @staticmethod
    def generate_social_content(medicine: Medicine) -> Dict[str, Any]:
        med_name = medicine.name
        animal = medicine.animal_type.name if medicine.animal_type else "สัตว์เลี้ยง"
        brand = medicine.brand or "เวชภัณฑ์คุณภาพ"
        indications = medicine.indications or "รักษาและดูแลสุขภาพ"
        price_str = f"฿{medicine.price:,.2f}" if medicine.price else "ราคาสุดคุ้ม"

        fb = f"FB POST: {med_name} จาก {brand} ตัวช่วยดูแล {animal} สรรพคุณ: {indications[:100]}... สั่งซื้อได้แล้ววันนี้ ที่ร้านของเรา! 💚 #ยาสัตว์ #{brand.replace(' ', '')}"
        ig = f"✨ {med_name}\nปกป้อง {animal} ให้แข็งแรงทุกวัน 🐾\n📍 {indications[:80]}...\n🛒 ราคา {price_str}\n#Veterinary #ดูแล{animal} #ยาสัตว์คุณภาพ"
        tiktok = f"🎬 คลิปนี้มีคำตอบ! วิธีดูแล {animal} เมื่อป่วยด้วย {med_name} 💊 ปลอดภัย ใช้ง่าย ผลลัพธ์ชัดเจน! กดตะกร้า/สั่งซื้อทักแชทเลย! #ยาสัตว์ #{animal}"
        line = f"💚 [LINE OA Broadcast] สวัสดีครับลูกค้า! ขอแนะนำ {med_name} สำหรับ {animal} สรรพคุณ: {indications[:80]}... กดคลิกเพื่อสอบถามราคาและสั่งซื้อผ่าน LINE ได้เลยครับ"
        website = f"บทความสินค้า: {med_name} เวชภัณฑ์ยาคุณภาพสำหรับ {animal} โดย {brand} สรรพคุณและขนาดการใช้ยาอย่างปลอดภัย..."

        hashtags = [f"#{med_name.replace(' ', '')}", f"#ดูแล{animal}", f"#ยาสัตว์{brand.replace(' ', '')}", "#เวชภัณฑ์สัตว์", "#สุขภาพสัตว์"]

        return {
            "facebook": fb,
            "instagram": ig,
            "tiktok": tiktok,
            "line_oa": line,
            "website": website,
            "hashtags": hashtags,
        }

    @staticmethod
    def generate_ideas() -> Dict[str, Any]:
        fb_ideas = [f"โพสต์ให้ความรู้เรื่องการสังเกตอาการป่วยไอ/หอบในสัตว์", "โพสต์เปรียบเทียบการดูแลสัตว์ก่อนและหลังใช้ยา", "โพสต์รีวิวจากเกษตรกรผู้ใช้งานจริงหน้าร้าน", "โพสต์ Q&A ตอบคำถามยอดฮิตเกี่ยวกับการฉีดยา", "โพสต์สรุประยะหยุดยาที่เกษตรกรต้องรู้"] * 6
        video_ideas = ["คลิปสาธิตวิธีเตรียมอุปกรณ์ฉีดยาอย่างถูกต้อง", "คลิป 3 ข้อผิดพลาดในการถ่ายพยาธิสัตว์", "คลิปพาทัวร์คลังยาและวิธีเก็บรักษายาหน้าร้าน", "คลิปถามตอบสัตวแพทย์ตอบปัญหาโรคสัตว์", "คลิปเตือนภัยโรคระบาดตามฤดูกาล"] * 6
        photo_ideas = ["ภาพถ่ายสินค้าคู่กับสัตว์เลี้ยงสุขภาพดี", "ภาพอินโฟกราฟิกสรุปขั้นตอนการใช้ยา", "ภาพซูมฉลากยาและจุดเด่นของตัวยาสำคัญ", "ภาพตารางคำนวณปริมาณยาตามน้ำหนักสัตว์", "ภาพถ่ายบรรยากาศหน้าร้านและการจัดส่งยา"] * 6
        promo_ideas = ["โปรโมชั่นซื้อยารักษาแถมวิตามินบำรุง", "โปรโมชั่นจัดส่งฟรีเมื่อซื้อครบ 1,000 บาท", "โปรโมชั่นต้อนรับฤดูฝนรับส่วนลด 10%", "โปรโมชั่นสะสมแต้มแลกรับส่วนลดหน้าร้าน", "โปรโมชั่นแพ็คเกจดูแลสัตว์ยกฝูง"] * 6
        edu_ideas = ["5 อาการเตือนภัยว่าสัตว์ของคุณกำลังติดพยาธิ", "ทำความรู้จักกับระยะหยุดยา (Withdrawal Period) คืออะไร", "วิธีการเก็บรักษายาสัตว์ในฤดูร้อนไม่ให้ยาเสื่อม", "ความแตกต่างระหว่างยาฉีดและยากินสำหรับปศุสัตว์", "วิธีดูแลแม่สัตว์หลังตกลูกอย่างปลอดภัย"] * 6

        return {
            "facebook_post_ideas": fb_ideas[:30],
            "video_ideas": video_ideas[:30],
            "photo_ideas": photo_ideas[:30],
            "promotion_ideas": promo_ideas[:30],
            "educational_content_ideas": edu_ideas[:30],
        }

    @staticmethod
    def generate_seo(medicine: Medicine) -> Dict[str, Any]:
        med_name = medicine.name
        animal = medicine.animal_type.name if medicine.animal_type else "สัตว์เลี้ยง"
        brand = medicine.brand or "แบรนด์ชั้นนำ"
        indications = medicine.indications or "รักษาโรคและดูแลสุขภาพสัตว์"

        meta_desc = f"ซื้อ {med_name} ({brand}) สำหรับ {animal} สรรพคุณ: {indications[:90]}... ของแท้ 100% สั่งซื้อออนไลน์หรือสอบถามราคาสุดคุ้มได้ที่นี่"
        keywords = [med_name, f"ยา{animal}", brand, f"ซื้อ {med_name}", f"สรรพคุณ {med_name}", "ยาสัตว์ออนไลน์", "ยาสัตว์ราคาถูก"]

        blog = f"""# คู่มือฉบับสมบูรณ์: การใช้ {med_name} เพื่อดูแล {animal} อย่างมีประสิทธิภาพและปลอดภัย

การดูแลสุขภาพของ {animal} เป็นหัวใจสำคัญของเกษตรกรและผู้เลี้ยงสัตว์ทุกคน หนึ่งในเวชภัณฑ์ที่ได้รับการยอมรับและใช้งานอย่างแพร่หลายคือ **{med_name}** จาก {brand}

## สรรพคุณและคุณประโยชน์ของ {med_name}
{indications}

## ขนาดและวิธีใช้งานอย่างถูกต้อง
{medicine.dosage or 'ควรใช้อย่างระมัดระวังตามคำแนะนำสัตวแพทย์'}

## ข้อควรระวังและระยะหยุดยา
{medicine.warnings or 'โปรดอ่านคำเตือนก่อนใช้ยา'}

สรุป: การเลือกใช้ {med_name} อย่างถูกวิธีตามคำแนะนำ จะช่วยให้ {animal} ของคุณกลับมาร่างกายแข็งแรงและเจริญเติบโตได้อย่างสมบูรณ์"""

        faq_schema = [
            {"question": f"{med_name} ใช้สำหรับรักษาอะไร?", "answer": indications},
            {"question": f"{med_name} มีวิธีใช้อย่างไร?", "answer": medicine.usage or medicine.dosage or "ใช้อย่างระมัดระวัง"},
        ]

        return {
            "product_description": f"{med_name} ({brand}) เวชภัณฑ์คุณภาพสูงสำหรับ {animal} สรรพคุณ: {indications}",
            "meta_description": meta_desc,
            "keywords": keywords,
            "blog_article": blog,
            "faq_schema": faq_schema,
        }

    @staticmethod
    def generate_calendar(medicine: Medicine) -> Dict[str, Any]:
        med_name = medicine.name
        animal = medicine.animal_type.name if medicine.animal_type else "สัตว์"
        
        days = []
        for i in range(1, 31):
            day_type = (i % 4)
            if day_type == 1:
                days.append({
                    "day": f"วันที่ {i}",
                    "facebook_post": f"แนะนำคุณประโยชน์ของ {med_name} ในการดูแล {animal}",
                    "promotion": "ส่วนลดพิเศษ 5% สำหรับสั่งซื้อวันนี้",
                    "educational_tip": f"💡 เคล็ดลับประจำวัน: วิธีสังเกตอาการป่วยเบื้องต้นใน {animal}",
                    "engagement_idea": "ถามคอมเมนต์: สัตว์เลี้ยงของคุณเคยมีอาการแบบนี้ไหม?"
                })
            elif day_type == 2:
                days.append({
                    "day": f"วันที่ {i}",
                    "facebook_post": f"เจาะลึกขนาดและวิธีฉีด/ให้ยา {med_name} อย่างถูกวิธี",
                    "promotion": "ซื้อ 2 ชิ้นรับของแถมพิเศษ",
                    "educational_tip": "💡 รู้หรือไม่: ทำไมระยะหยุดยาถึงมีความสำคัญต่อคนบริโภค",
                    "engagement_idea": "โพสต์รูปถ่ายสัตว์เลี้ยงคู่กับขวดยาหน้าร้าน"
                })
            elif day_type == 3:
                days.append({
                    "day": f"วันที่ {i}",
                    "facebook_post": f"ไขข้อข้องใจ! รวม FAQ คำถามยอดฮิตเกี่ยวกับ {med_name}",
                    "promotion": "จัดส่งฟรีเมื่อสั่งซื้อสินค้าในหมวดหมู่นี้",
                    "educational_tip": "💡 วิธีการเก็บรักษายาให้คงประสิทธิภาพยาวนาน",
                    "engagement_idea": "ชวนร่วมกิจกรรมโหวต: ปัญหาไหนที่คุณเจอบ่อยที่สุดในการเลี้ยงสัตว์?"
                })
            else:
                days.append({
                    "day": f"วันที่ {i}",
                    "facebook_post": f"รีวิวความประทับใจและผลลัพธ์จากการใช้ {med_name}",
                    "promotion": "โปรโมชั่นพิเศษวันสุดท้ายของสัปดาห์",
                    "educational_tip": f"💡 การดูแลโภชนาการควบคู่กับการใช้ยาใน {animal}",
                    "engagement_idea": "แจกโค้ดส่วนลดพิเศษให้ 5 คอมเมนต์แรก"
                })
        return {"calendar_30_days": days}

    @staticmethod
    def generate_one_click(medicine: Medicine) -> Dict[str, Any]:
        copy_res = AIMarketingService.generate_marketing_copy(medicine, tone="Professional")
        prompt_res = AIMarketingService.generate_image_prompts(medicine, color_theme="Green & Gold", marketing_goal="Poster")
        social_res = AIMarketingService.generate_social_content(medicine)
        seo_res = AIMarketingService.generate_seo(medicine)
        ideas_res = AIMarketingService.generate_ideas()

        return {
            "medicine_name": medicine.name,
            "facebook_post": copy_res["facebook_post"],
            "short_caption": copy_res["short_caption"],
            "long_caption": copy_res["long_caption"],
            "headline": copy_res["headline"],
            "promotion_text": copy_res["promotional_text"],
            "poster_prompt": prompt_res["portrait_prompt"],
            "instagram_caption": social_res["instagram"],
            "tiktok_caption": social_res["tiktok"],
            "line_oa_broadcast": social_res["line_oa"],
            "hashtags": social_res["hashtags"],
            "seo_description": seo_res["meta_description"],
            "marketing_ideas": ideas_res["facebook_post_ideas"][:5],
        }
