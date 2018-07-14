from db import db_session, Book, Page
from datetime import datetime
from emoji import emojize

def new_book(b_name,o_id):
	book_item=Book(book_name=b_name, owner_id=o_id, created=datetime.now(), updated=datetime.now())
	db_session.add(book_item)
	db_session.commit()

def delete_book(bid):
	for pagelist in Page.query.filter_by(book_id=bid).all():
		Page.query.filter_by(id=pagelist.id).delete()
	Book.query.filter_by(id=bid).delete()
	db_session.commit()

def book_list(uid):
	blist=Book.query.filter_by(owner_id=uid).all()
	return blist

def new_book_page(bid,p_name,p_content):
	nbpage = Page(page_name=p_name, page_content=p_content, created=datetime.now(), updated=datetime.now(), book_id =bid)
	db_session.add(nbpage)
	db_session.commit()

def page_list(bid):
	plist=Page.query.filter_by(book_id=bid).all()
	return plist

def drop_page(bid,pid):
	Page.query.filter_by(book_id=bid, id=pid).delete()
	db_session.commit()