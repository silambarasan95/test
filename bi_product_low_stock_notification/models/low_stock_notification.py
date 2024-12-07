# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields,models,api, _
from ast import literal_eval
from odoo import SUPERUSER_ID
import base64
from odoo.exceptions import UserError


class LowStockNotification(models.Model):
	_name="low.stock.notification"
	_description="Low Stock Notification"

	company_id = fields.Many2one('res.company','Company')
	low_stock_products_ids = fields.One2many(related='company_id.low_stock_products_ids',string="Low Stock")

	def action_list_products_(self):

		products_list=[]
		
		products_dlt = [(2,dlt.id,0)for dlt in self.env.company.low_stock_products_ids]
		self.env.company.low_stock_products_ids = products_dlt
	
		if self.env.company.notification_base == 'on_hand':
			if self.env.company.notification_products == 'for_all':

				if self.env.company.notification_product_type == 'variant':
					result = self.env['product.product'].search([('qty_available','<',self.env.company.min_quantity),
															   ('detailed_type','=','product')])
					for product in result:
						name_att = ' '
						for attribute in product.product_template_attribute_value_ids:
						  name_att = name_att  +  attribute.name + '  '

						name_pro = ' '
						if product.product_template_attribute_value_ids :
						  name_pro = product.name + ' - ' +name_att + '  '
						else :
						  name_pro = product.name

						products_list.append([0,0,{'name':name_pro,
											  'limit_quantity':self.env.company.min_quantity,
											  'stock_quantity':product.qty_available,
											 }])

				else:
					result = self.env['product.template'].search([('detailed_type','=','product')])
					for product in result:
						if product.qty_available < self.env.company.min_quantity:
							products_list.append([0,0,{'name':product.name,
												  'limit_quantity':self.env.company.min_quantity,
												  'stock_quantity':product.qty_available}])

			if self.env.company.notification_products == 'fore_product':
				if self.env.company.notification_product_type == 'variant':               
					result = self.env['product.product'].search([('detailed_type','=','product')])
	
					for product in result:
						if product.qty_available < product.min_quantity:
							name_att = ' '
							for attribute in product.product_template_attribute_value_ids:
							  name_att = name_att  +  attribute.name + '  '

							name_pro = ' '
							if product.product_template_attribute_value_ids :
							  name_pro = product.name + ' - ' +name_att + '  '
							else :
							  name_pro = product.name
							
							products_list.append([0,0,{'name':name_pro,
													  'limit_quantity':product.min_quantity,
												  'stock_quantity':product.qty_available,}])
				else:
					result = self.env['product.template'].search([('detailed_type','=','product')])

					for product in result:
						if product.qty_available < product.temp_min_quantity:
							products_list.append([0,0,{'name':product.name,
											  'limit_quantity':product.temp_min_quantity,
											  'stock_quantity':product.qty_available}])

			if self.env.company.notification_products == 'reorder':

				if self.env.company.notification_product_type == 'variant':                  
					result = self.env['product.product'].search([('detailed_type','=','product')])
					#print('************************',len(result))
					for product in result:
						if product.qty_available < product.qty_min:
							name_att = ' '
							for attribute in product.product_template_attribute_value_ids:
							  name_att = name_att  +  attribute.name + '  '

							name_pro = ' '
							if product.product_template_attribute_value_ids :
							  name_pro = product.name + ' - ' +name_att + '  '
							else :
							  name_pro = product.name
							vals = {'name':name_pro,
								  'limit_quantity':product.qty_min,
								  'stock_quantity':product.qty_available}

							products_list.append([0,0,vals])
							#print('666666666666666666666',len(products_list))

				else:
					result = self.env['product.template'].search([('detailed_type','=','product')])
					for product in result:
						if product.qty_available < product.temp_qty_min:
						  products_list.append([0,0,{'name':product.name,
											  'limit_quantity':product.temp_qty_min,
											  'stock_quantity':product.qty_available}])
						  #print('55555555555555555',len(products_list))

		if self.env.company.notification_base=='fore_cast':
			if self.env.company.notification_products=='for_all':

				if self.env.company.notification_product_type == 'variant':
					result = self.env['product.product'].search([('virtual_available','<',self.env.company.min_quantity),
															   ('detailed_type','=','product')])
					for product in result:
						name_att = ' '
						for attribute in product.product_template_attribute_value_ids:
						  name_att = name_att  +  attribute.name + '  '

						name_pro = ' '
						if product.product_template_attribute_value_ids :
						  name_pro = product.name + ' - ' +name_att + '  '

						else :
						  name_pro = product.name

						products_list.append([0,0,{'name':name_pro,
											  'limit_quantity':self.env.company.min_quantity,
											  'stock_quantity':product.virtual_available}])
				else:
					result = self.env['product.template'].search([])

					for product in result:
						if product.virtual_available < self.env.company.min_quantity:
						  products_list.append([0,0,{'name':product.name,
											  'limit_quantity':self.env.company.min_quantity,
											  'stock_quantity':product.virtual_available}])


			if self.env.company.notification_products == 'fore_product':
				
				if self.env.company.notification_product_type == 'variant':
					result = self.env['product.product'].search([('detailed_type','=','product')])

					for product in result:
						if product.virtual_available < product.min_quantity:
							name_att = ' '
							for attribute in product.product_template_attribute_value_ids:
							  name_att = name_att  +  attribute.name + '  '

							name_pro = ' '
							if product.product_template_attribute_value_ids :
							  name_pro = product.name + ' - ' +name_att + '  '
							else :
							  name_pro = product.name
							products_list.append([0,0,{'name':name_pro,
													  'limit_quantity':product.min_quantity,
												  'stock_quantity':product.virtual_available}])
				
				else:
					result = self.env['product.template'].search([('detailed_type','=','product')])

					for product in result:
						if product.virtual_available < product.temp_min_quantity:
							products_list.append([0,0,{'name':product.name,
											  'limit_quantity':product.temp_min_quantity,
											  'stock_quantity':product.virtual_available}])

			if self.env.company.notification_products == 'reorder':

				if self.env.company.notification_product_type == 'variant':                  
					result = self.env['product.product'].search([('detailed_type','=','product')])
					for product in result:
						if product.virtual_available < product.qty_min:
							name_att = ' '
							for attribute in product.product_template_attribute_value_ids:
							  name_att = name_att  +  attribute.name + '  '

							name_pro = ' '
							if product.product_template_attribute_value_ids :
							  name_pro = product.name + ' - ' +name_att + '  '
							else :
							  name_pro = product.name

							products_list.append([0,0,{'name':name_pro,
													  'limit_quantity':product.qty_min,
												  'stock_quantity':product.virtual_available}])
				else:
					result = self.env['product.template'].search([('detailed_type','=','product')])

					for product in result:
						if product.virtual_available < product.temp_qty_min:
							products_list.append([0,0,{'name':product.name,
											  'limit_quantity':product.temp_qty_min,
											  'stock_quantity':product.virtual_available}])
		
		self.env.company.low_stock_products_ids = products_list
		
		return
	def action_low_stock_send(self):
		context = self._context
		current_uid = context.get('uid')
		su_id = self.env['res.users'].browse(current_uid)
		self.action_list_products_()
		companies = self.env['res.company'].search([('notify_low_stock', '=', True)])
		res = self.env['res.config.settings'].search([], order="id desc", limit=1)
		if su_id:
			current_user = su_id
		else:
			current_user = self.env.user
		if self.env.company.low_stock_products_ids:
			for company in companies:
				if company.email:  # Ensure the company has an email address
					try:
						notification_products = self.env.company.notification_products
						notification_base = self.env.company.notification_base 
						if notification_products == 'for_all':
							subject = f"Low Stock Notification for Global {'OnHand' if notification_base == 'on_hand' else 'ForeCast'} Products"
						elif notification_products == 'fore_product':
							subject = f"Low Stock Notification for Individual {'OnHand' if notification_base == 'on_hand' else 'ForeCast'} Products"
						elif notification_products == 'reorder':
							subject = f"Low Stock Notification for Individual Reorder Rules Products"
						else:
							subject = "Low Stock Notification for Products"
						body_html = self._construct_email_body(company)
						pdf = self.env['ir.actions.report']._render_qweb_pdf("bi_product_low_stock_notification.action_low_stock_report", res.id)
						mail_values = {
	                        'subject': subject,
	                        'body_html': body_html,
	                        'email_from': current_user.email,
	                        'email_to': company.email,
	                        'attachment_ids': [(0, 0, {
	                            'name': 'Product Low Stock Report',
	                            'datas': base64.b64encode(pdf[0]),
	                            'res_model': self._name,
	                            'res_id': self.id,
	                            'mimetype': 'application/pdf',
	                            'type': 'binary',
	                        })],
	                    }
						mail_mail_obj = self.env['mail.mail']
						msg_id = mail_mail_obj.create(mail_values)
						if msg_id:
							msg_id.send()
					except Exception as e:
						raise UserError(_("Failed to send email to %s: %s") % (company.email, str(e)))
			users_to_notify = self.env['res.users'].search([('notify_user', '=', True)])
			for partner in users_to_notify:
				###print(partner.name)
				try:
					notification_products = self.env.company.notification_products
					notification_base = self.env.company.notification_base 
					if notification_products == 'for_all':
						subject = f"Low Stock Notification for Global {'OnHand' if notification_base == 'on_hand' else 'ForeCast'} Products"
					elif notification_products == 'fore_product':
						subject = f"Low Stock Notification for Individual {'OnHand' if notification_base == 'on_hand' else 'ForeCast'} Products"
					elif notification_products == 'reorder':
						subject = f"Low Stock Notification for Individual Reorder Rules Products"
					else:
						subject = "Low Stock Notification for Products"
					body_html = self._construct_email_body(company)
					pdf = self.env['ir.actions.report']._render_qweb_pdf("bi_product_low_stock_notification.action_low_stock_report", res.id)
					mail_values = {
	                        'subject': subject,
	                        'body_html': body_html,
	                        'email_from': current_user.email,
	                        'email_to': partner.email,
	                        'attachment_ids': [(0, 0, {
	                            'name': 'Product Low Stock Report',
	                            'datas': base64.b64encode(pdf[0]),
	                            'res_model': self._name,
	                            'res_id': self.id,
	                            'mimetype': 'application/pdf',
	                            'type': 'binary',
	                        })],
	                    }
					mail_mail_obj = self.env['mail.mail']
					msg_id = mail_mail_obj.create(mail_values)
					if msg_id:
						msg_id.send()
				except Exception as e:
					raise UserError(_("Failed to send email to %s: %s") % (company.email, str(e)))
		return True
	
	def _construct_email_body(self, company):
	    body_html = """
	        <p>Dear {},</p>
	        <p>We would like to inform you that the following products are low in stock:</p>
	        <table style="border-collapse: collapse; width: 100%;">
	            <thead>
	                <tr style="background-color: #f2f2f2;">
	                    <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;" colspan="4">Low Stock Notification</th>
	                </tr>
	                <tr style="background-color: #f2f2f2;">
	                    <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Product</th>
	                    <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Minimum Quantity</th>
	                    <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Product Quantity</th>
	                    <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Required Quantity</th>
	                </tr>
	            </thead>
	            <tbody>
	    """.format(company.name)
	
	    for product in self.env.company.low_stock_products_ids:
	        body_html += """
	            <tr>
	                <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
	                <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
	                <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
	                <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
	            </tr>
	        """.format(product.name, self.env.company.min_quantity, product.stock_quantity, (self.env.company.min_quantity - product.stock_quantity))
	
	    body_html += """
	            </tbody>
	        </table>
	        <p>Best regards,<br/>Your Company</p>
	    """
	    return body_html

# @api.model
# def action_low_stock_send(self):
# 	context = self._context
# 	current_uid = context.get('uid')
# 	current_user = self.env['res.users'].browse(current_uid) if current_uid else self.env.user
# 	self.action_list_products_()  # Ensure this method is defined correctly
# 	companies = self.env['res.company'].search([('notify_low_stock', '=', True)])
# 	res = self.env['res.config.settings'].search([], order="id desc", limit=1)
# 	if self.env.company.low_stock_products_ids:
# 		for company in companies:
# 			if company.email:  # Ensure the company has an email address
# 				try:
# 					body_html = "<p>Dear {},</p><p>We would like to inform you that the following products are low in stock:</p>".format(company.name)
# 					for product in self.env.company.low_stock_products_ids:
# 						body_html += "<p>Product: {} - Available Quantity: {}</p>".format(product.name, product.quantity_available)
# 					body_html += "<p>Best regards,<br/>Your Company</p>"
# 					pdf = self.env['ir.actions.report']._render_qweb_pdf("bi_product_low_stock_notification.action_low_stock_report", res.id)
# 					mail_values = {
#                            'subject': subject,
#                            'body_html': body_html,
#                            'email_from': current_user.email,
#                            'email_to': company.email,
#                            'attachment_ids': [(0, 0, {
#                                'name': 'Product Low Stock Report',
#                                'datas': base64.b64encode(pdf[0]),
#                                'res_model': self._name,
#                                'res_id': self.id,
#                                'mimetype': 'application/pdf',
#                                'type': 'binary',
#                            })],
#                        }
# 					mail_mail_obj = self.env['mail.mail']
#                        msg_id = mail_mail_obj.create(mail_values)
#                        if msg_id:
#                            msg_id.send()
#
#                    except Exception as e:
#                        raise UserError(_("Failed to send email to %s: %s") % (company.email, str(e)))

            # # Notify users who want low stock notifications
            # users_to_notify = self.env['res.users'].search([('notify_user', '=', True)])
            # for user in users_to_notify:
            #     if user.email:  # Ensure the user has an email address
            #         try:
            #             # Prepare email values
            #             subject = "Low Stock Notification for Products"
            #             body_html = "<p>Dear {},</p><p>We would like to inform you that some products are low in stock.</p>".format(user.name)
            #
            #             # Generate PDF attachment
            #             pdf = self.env['ir.actions.report']._render_qweb_pdf("bi_product_low_stock_notification.action_low_stock_report", res.id)
            #
            #             # Create email message
            #             mail_values = {
            #                 'subject': subject,
            #                 'body_html': body_html,
            #                 'email_from': current_user.email,
            #                 'email_to': user.email,
            #                 'attachment_ids': [(0, 0, {
            #                     'name': 'Product Low Stock Report',
            #                     'datas': base64.b64encode(pdf[0]),
            #                     'res_model': self._name,
            #                     'res_id': self.id,
            #                     'mimetype': 'application/pdf',
            #                     'type': 'binary',
            #                 })],
            #             }
            #
            #             # Create and send email
            #             mail_mail_obj = self.env['mail.mail']
            #             msg_id = mail_mail_obj.create(mail_values)
            #             if msg_id:
            #                 msg_id.send()
            #
            #         except Exception as e:
            #             raise UserError(_("Failed to send email to %s: %s") % (user.email, str(e)))

        #return True 

# 	def action_low_stock_send(self):
#
# 		context = self._context
# 		current_uid = context.get('uid')
# 		su_id = self.env['res.users'].browse(current_uid)
# 		self.action_list_products_()
# 		companies = self.env['res.company'].search([('notify_low_stock','=',True)])
# 		res = self.env['res.config.settings'].search([],order="id desc", limit=1)
# 		if su_id :
# 			current_user = su_id
# 		else:
# 			current_user = self.env.user
# 		# if res.id :
# 		if self.env.company.low_stock_products_ids:
# 			#if company:
# 			for company in companies:
# 				if company.email:  # Ensure the company has an email address
# 					try:
# 						notification_products = self.env.company.notification_products
# 						notification_base = self.env.company.notification_base 
# 						if notification_products == 'for_all':
# 							if notification_base == 'on_hand':
# 								subject = "Low Stock Notification for Global OnHand Products"
# 							elif notification_base == 'fore_cast':
# 								subject = "Low Stock Notification for Global ForeCast Products"
# 						elif notification_products == 'fore_product':
# 							if notification_base == 'on_hand':
# 								subject = "Low Stock Notification for Individual OnHand Products"
# 							elif notification_base == 'fore_cast':
# 								subject = "Low Stock Notification for Individual ForeCast Products"
# 						elif notification_products == 'reorder':
# 							if notification_base == 'on_hand':
# 								subject = "Low Stock Notification for Individual reorder rules Products"
# 							elif notification_base == 'fore_cast':
# 								subject = "Low Stock Notification for Individual reorder rules Products"
# 						else:
# 								subject = "Low Stock Notification for Products"
# 						#print(subject)
# 						body_html = "<p>Dear {},</p><p>We would like to inform you that the following products are low in stock:</p>".format(company.name)
# 						body_html = """
# 									<p>Dear {},</p>
# 									<p>We would like to inform you that the following products are low in stock:</p>
# 									<table style="border-collapse: collapse; width: 100%;">
# 									    <thead>
# 									        <tr style="background-color: #f2f2f2;">
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;" colspan="4">Low Stock Notification</th>
# 									        </tr>
# 									        <tr style="background-color: #f2f2f2;">
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Product</th>
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Minimum Quantity</th>
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Product Quantity</th>
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Required Quantity</th>
# 									        </tr>
# 									    </thead>
# 									    <tbody>
# 									""".format(company.name)
# 						for product in self.env.company.low_stock_products_ids:
# 							#print(product.name)
# 							# Start the HTML table with a single header row
# 							body_html += """
# 								        <tr>
# 								            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
# 								            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
# 								            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
# 								            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
# 								        </tr>
# 								    """.format(product.name, self.env.company.min_quantity, product.stock_quantity, (self.env.company.min_quantity - product.stock_quantity))
#
# # Close the table tag
# 						body_html += """
# 									    </tbody>
# 									</table>
# 									"""
#
# 						body_html += "<p>Best regards,<br/>Your Company</p>"
# 						#print(body_html)
# 						pdf = self.env['ir.actions.report']._render_qweb_pdf("bi_product_low_stock_notification.action_low_stock_report", res.id)
# 						mail_values = {
# 					'subject': subject,
# 					'body_html': body_html,
# 					'email_from': current_user.email,
# 					'email_to': company.email,
# 					'attachment_ids': [(0, 0, {
# 					'name': 'Product Low Stock Report',
# 					'datas': base64.b64encode(pdf[0]),
# 					'res_model': self._name,
# 					'res_id': self.id,
# 					'mimetype': 'application/pdf',
# 					'type': 'binary',
# 					})],
# 					}
# 						mail_mail_obj = self.env['mail.mail']
# 						msg_id = mail_mail_obj.create(mail_values)
# 						if msg_id:
# 							msg_id.send()
# 					except Exception as e:
# 						raise UserError(_("Failed to send email to %s: %s") % (company.email, str(e)))
# 		return 	True
	  	#users_to_notify = self.env['res.users'].search([('notify_user', '=', True)])
    # for partner in users_to_notify:
    #   	#print('----------------------------',partner.name)
    #   	#if partner.notify_user:
    #   	try:
    #   	    template_id = self.env['ir.model.data']._xmlid_lookup('bi_product_low_stock_notification.low_stock_email_template')
    #   	except IndexError:
    #   	    raise UserError(_("The email template 'low_stock_email_template' is missing. Please ensure it exists."))
    #   	email_template_obj = self.env['mail.template'].browse(template_id)
    #   	if template_id:
    #   		values = email_template_obj.generate_email(self.id,['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
    #   		values['email_from'] = current_user.email
    #   		values['email_to'] = partner.email
    #   		#print('----------------------------',partner.email)
    #   		values['author_id'] = current_user.partner_id.id
    #   		values['res_id'] = False
    #   		pdf = self.env['ir.actions.report']._render_qweb_pdf("bi_product_low_stock_notification.action_low_stock_report", res.id)
    #   		values['attachment_ids'] = [(0,0,{
    #   				'name': 'Product Low Stock Report',
    #   				'datas': base64.b64encode(pdf[0]),
    #   				'res_model': self._name,
    #   				'res_id': self.id,
    #   				'mimetype': 'application/pdf',
    #   				'type': 'binary',
    #   				})]
    #   		mail_mail_obj = self.env['mail.mail']
    #   		msg_id = mail_mail_obj.create(values)
    #   		if msg_id:
    #   			msg_id.send()
	  
	  	

	#return True
# 	def action_low_stock_send(self):
#
# 		context = self._context
# 		current_uid = context.get('uid')
# 		su_id = self.env['res.users'].browse(current_uid)
# 		self.action_list_products_()
# 		companies = self.env['res.company'].search([('notify_low_stock','=',True)])
# 		res = self.env['res.config.settings'].search([],order="id desc", limit=1)
# 		if su_id :
# 			current_user = su_id
# 		else:
# 			current_user = self.env.user
# 		# if res.id :
# 		if self.env.company.low_stock_products_ids:
# 			#if company:
# 			for company in companies:
# 				if company.email:  # Ensure the company has an email address
# 					#try:
#       # notification_products = self.env.company.notification_products
#       # notification_base = self.env.company.notification_base 
#       # if notification_products == 'for_all':
#       # 	if notification_base == 'on_hand':
#       # 		subject = "Low Stock Notification for Global OnHand Products"
#       # 	elif notification_base == 'fore_cast':
#       # 		subject = "Low Stock Notification for Global ForeCast Products"
#       # elif notification_products == 'fore_product':
#       # 	if notification_base == 'on_hand':
#       # 		subject = "Low Stock Notification for Individual OnHand Products"
#       # 	elif notification_base == 'fore_cast':
#       # 		subject = "Low Stock Notification for Individual ForeCast Products"
#       # elif notification_products == 'reorder':
#       # 	if notification_base == 'on_hand':
#       # 		subject = "Low Stock Notification for Individual reorder rules Products"
#       # 	elif notification_base == 'fore_cast':
#       # 		subject = "Low Stock Notification for Individual reorder rules Products"
#       # else:
# 						subject = "Low Stock Notification for Products"
# 						#print(subject)
# 						#body_html = "<p>Dear {},</p><p>We would like to inform you that the following products are low in stock:</p>".format(company.name)
# 						body_html = """
# 									<p>Dear {},</p>
# 									<p>We would like to inform you that the following products are low in stock:</p>
# 									<table style="border-collapse: collapse; width: 100%;">
# 									    <thead>
# 									        <tr style="background-color: #f2f2f2;">
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;" colspan="4">Low Stock Notification</th>
# 									        </tr>
# 									        <tr style="background-color: #f2f2f2;">
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Product</th>
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Minimum Quantity</th>
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Product Quantity</th>
# 									            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px;">Required Quantity</th>
# 									        </tr>
# 									    </thead>
# 									    <tbody>
# 									""".format(company.name)
# 						for product in self.env.company.low_stock_products_ids:
# 							#print(product.name)
# 							# Start the HTML table with a single header row
# 							body_html += """
# 								        <tr>
# 								            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
# 								            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
# 								            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
# 								            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{}</td>
# 								        </tr>
# 								    """.format(product.name, self.env.company.min_quantity, product.stock_quantity, (self.env.company.min_quantity - product.stock_quantity))
#
# # Close the table tag
# 						body_html += """
# 									    </tbody>
# 									</table>
# 									"""
#
# 						body_html += "<p>Best regards,<br/>Your Company</p>"
# 						#print(body_html)
# 						pdf = self.env['ir.actions.report']._render_qweb_pdf("bi_product_low_stock_notification.action_low_stock_report", res.id)
# 						mail_values = {
# 					'subject': subject,
# 					'body_html': body_html,
# 					#'email_from': current_user.email,
# 					#'email_to': company.email,
# 					'attachment_ids': [(0, 0, {
# 					'name': 'Product Low Stock Report',
# 					'datas': base64.b64encode(pdf[0]),
# 					'res_model': self._name,
# 					'res_id': self.id,
# 					'mimetype': 'application/pdf',
# 					'type': 'binary',
# 					})],
# 					}
# 						mail_mail_obj = self.env['mail.mail']
# 						msg_id = mail_mail_obj.create(mail_values)
# 						if msg_id:
# 							msg_id.send()
# 					#except Exception as e:
# 						#raise UserError(_("Failed to send email to %s: %s") % (company.email, str(e)))
# 			return True

        # Notify users
        # users_to_notify = self.env['res.users'].search([('notify_user', '=', True)])
        # for partner in users_to_notify:
        #     try:
        #         template_id = self.env['ir.model.data']._xmlid_lookup('bi_product_low_stock_notification.low_stock_email_template')
        #     except IndexError:
        #         raise UserError(_("The email template 'low_stock_email_template' is missing. Please ensure it exists."))
        #
        #     email_template_obj = self.env['mail.template'].browse(template_id[0])
        #     if template_id:
        #         values = email_template_obj.generate_email(self.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
        #         values['email_from'] = current_user.email
        #         values['email_to'] = partner.email
        #         values['author_id'] = current_user.partner_id.id
        #         values['res_id'] = False
        #
        #         # Generate PDF report
        #         pdf = self.env['ir.actions.report']._render_qweb_pdf("bi_product_low_stock_notification.action_low_stock_report", res.id)
        #         values['attachment_ids'] = [(0, 0, {
        #             'name': 'Product Low Stock Report',
        #             'datas': base64.b64encode(pdf[0]),
        #             'res_model': self._name,
        #             'res_id': self.id,
        #             'mimetype': 'application/pdf',
        #             'type': 'binary',
        #         })]
        #
        #         mail_mail_obj = self.env['mail.mail']
        #         msg_id = mail_mail_obj.create(values)
        #         if msg_id:
        #             msg_id.send()
        #     except Exception as e:
        #         raise UserError(_("Failed to send email to %s: %s") % (partner.email, str(e)))

    	





class LowstockLine(models.Model):
	_name='low.stock.line'
	_description="Low Stock Line"

	name=fields.Char(string='Product name')
	stock_quantity=fields.Float(string='Quantity')
	limit_quantity=fields.Float(string='Quantity limit')
	stock_product_id=fields.Many2one('low.stock.notification')
	new_product_id = fields.Many2one('product.product')