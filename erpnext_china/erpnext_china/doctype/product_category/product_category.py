# Copyright (c) 2024, Digitwise Ltd. and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.desk.search import search_widget
from frappe.model.document import Document


class ProductCategory(Document):
	pass

@frappe.whitelist()
def update_sorted_index(**kwargs):
	sorted_index = kwargs.get('sorted')
	if sorted_index:
		sorted_index = json.loads(sorted_index)
		for i in sorted_index:
			doc = frappe.get_doc("Product Category", i.get('name'))
			doc.sorted_index = int(i.get('index'))
			doc.save(ignore_permissions=True)

@frappe.whitelist()
def custom_product_category_query(doctype, txt, searchfield, start, page_len, filters):
	"""
	根据sorted_index升序排列
	"""
	results = search_widget(
		doctype,
		txt.strip(),
		searchfield=searchfield,
		page_length=page_len,
		filters=filters,
	)
	names = frappe.get_all("Product Category", filters=[
		["name", 'in', [res[0] for res in results]]
    ], order_by="sorted_index asc", pluck="name")
	return [(name, )for name in names]
