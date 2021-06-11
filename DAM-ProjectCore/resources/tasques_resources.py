import falcon
from sqlalchemy.exc import IntegrityError

from hooks import requires_auth
from resources.base_resources import DAMCoreResource
from db.models import  Book

import messages
from db.json_model import JSONModel
import settings 

@falcon.before(requires_auth)
class ResourceCreateTask(DAMCoreResource):
    def on_post(self,req,resp,*args,**kwargs):
        super(ResourceCreateBook, self).on_post(req,resp,*args,**kwargs)
        
        book = Book()
        
        
        #Request Body --> {tittle:value1, description:value2} raw-json
        
        try:
            book.tittle = req.media["tittle"] #NOM DE LA CLAU QUE VA AL BODY DEL POSTMAN, si fessim req.get_param("KEY") podriem fer postman amb Params
            book.description = req.media["description"]
            self.db_session.add(book)
            try:
                self.db_session.commit()
            except IntegrityError:
                raise falcon.HTTPBadRequest("El llibre ja existeix")
                
        except KeyError:
            raise falcon.HTTPBadRequest("Per poder donar d'alta llibre necessito clau titol i descripcio")
        
        resp.status = falcon.HTTP_200
        
        
@falcon.before(requires_auth)      
class ResourceFindBookById(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceFindBookById, self).on_get(req,resp,*args,**kwargs) 

        id = req.get_param("id") #pel param li passem una ID
        
        
        if id is not None:
            book = self.db_session.query(Book).filter(Book.id == id).one_or_none() # a book guardem l'objecte que retorna la BD
            if book is not None:
                resp.media = book.json_model  #Resp es x enviar respostes, enviem el objecte book com a JSONModel
                resp.status = falcon.HTTP_200
            else:
                raise falcon.HTTPBadRequest("El llibre no existeix")

        else:
            raise falcon.HTTPBadRequest("Cal que passis una ID per trobar llibres")
            
        resp.status = falcon.HTTP_200



class ResourceUpdateBook(DAMCoreResource):
    def on_put(self,req,resp,*args,**kwargs):
        super(ResourceUpdateBook, self).on_put(req,resp,*args,**kwargs) 
        
        try:
            tittle = req.media["tittle"] ##INFORMACIÓ A LA QUE ACTUALITZA Q LI PASSEM PEL BODY
            description = req.media["description"]
        
            id = req.get_param("id") #pel param li passem una ID
            if id is not None:
                book = self.db_session.query(Book).filter(Book.id == id).one_or_none()
                if book is not None:
                    book.tittle = tittle
                    book.description = description #li posem les dades que hem agafat de les linies 63-64 amb el body a postman
                    self.db_session.commit()
                else: 
                    raise falcon.HTTPBadRequest("no existeix el llibre") #podem fer que crei el llibre si vulguessim aquí.
            else:
                raise falcon.HTTPBadRequest("per actualitzar un llibre necessito que posis la ID")
        
        except KeyError:     
                raise falcon.HTTPBadRequest("El body JSON ha de tenir claus tittle i description")
        
        resp.status = falcon.HTTP_200
        
        
        
class ResourceDeleteBook(DAMCoreResource):
    def on_delete(self,req,resp,*args,**kwargs):
        super(ResourceDeleteBook, self).on_delete(req,resp,*args,**kwargs) 
           
        id = req.get_param("id") #pel param li passem una ID
        if id is not None:
            book = self.db_session.query(Book).filter(Book.id == id).one_or_none()
            if book is not None:
                self.db_session.delete(book)
                self.db_session.commit()
            else: 
                raise falcon.HTTPBadRequest("no existeix el llibre") #podem fer que crei el llibre si vulguessim aquí.
        else:
            raise falcon.HTTPBadRequest("per actualitzar un llibre necessito que posis la ID")
       
        resp.status = falcon.HTTP_200

@falcon.before(requires_auth)      
class ResourceGetBook(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetBook, self).on_get(req,resp,*args,**kwargs)
        
        books = list()
        _query = self.db_session.query(Book) #BUSCA TOT EL QUE HI HAGI A LA BASE DE DADES A LA TAULA BOOK I POSAU A query
        
        
        #filter
        genres = req.get_param("genres")
        
        if genres is not None:
            _query = _query.filter(Book.genre == genres)
        
        results = _query.all()
     
        '''results = query.all()#retornam tot el que hi hagi a query
        results = query.limit(3)#retornam nomes 3'''
                       
        for book in results:
            books.append(book.custom) #Si enlloc de custom escribissim 
            
        resp.media = books #enviem tot l'array
        
        
@falcon.before(requires_auth)      
class ResourceGetBookAdvance(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetBookAdvance, self).on_get(req,resp,*args,**kwargs)
        
        books = list()
        _query = self.db_session.query(Book) #BUSCA TOT EL QUE HI HAGI A LA BASE DE DADES A LA TAULA BOOK I POSAU A query
        
        
        #filter per genres diferents
        genres = req.get_param("genres")
        
        if genres is not None:
            genres_list = genres.split(",") #array amb paraules separades per comes
            _query = _query.filter(Book.genre.in_(genres_list)) #filtrem per més d'una categoria ara, totes les que tingui a la llista.
        
        
        #SORTING
        sort_field = req.get_param("sort_field")
        sort_fields = ["height","tittle","genre"] #els diferents sorts que permetre
        sort_type= req.get_param("sort_type")
        
        
        if sort_field in sort_fields and sort_type == "ASC":
            _query = _query.order_by(getattr(Book,sort_field).asc())
        
        elif sort_field in sort_fields and sort_type == "DESC":
            _query = _query.order_by(getattr(Book,sort_field).asc())
        else:
            raise falcon.HTTPBadRequest("Per ordenar necessito un sort_field = height,tittle o genre i un sort_type igual a ASC o DESC")
        '''if sort_type == "ASC":
            _query = _query.order_by(Book.height.asc())
        
        if sort_type == "DESC":
            _query = _query.order_by(Book.height.desc())'''

        results = _query.all()
     
        '''results = query.all()#retornam tot el que hi hagi a query
        results = query.limit(3)#retornam nomes 3'''
                       
        for book in results:
            books.append(book.custom) #Si enlloc de custom escribissim 
            
        resp.media = books #enviem tot l'array

##-----------------------EXAMEN------------------------------
'''@falcon.before(requires_auth)
class ResourceCreateTask(DAMCoreResource):
    def on_post(self,req,resp,*args,**kwargs):
        super(ResourceCreateTask, self).on_post(req,resp,*args,**kwargs)
        
        task = Task()
        
        
        #Request Body --> {tittle:value1, description:value2} raw-json
        
        try:
            task.name = req.get_param("name") #NOM DE LA CLAU QUE VA AL BODY DEL POSTMAN, si fessim req.get_param("KEY") podriem fer postman amb Params
            task.description = req.get_param("description")	    
	    task.hours = req.get_param("hours")
	    task.completed = req.get_param("completed")
            self.db_session.add(task)
            try:
                self.db_session.commit()
            except IntegrityError:
                raise falcon.HTTPBadRequest("LA TASCA EXISTEIX JA")
                
        except KeyError:
            raise falcon.HTTPBadRequest("PER PODER FER UN LLIBRE NECESSITO MÍNIM QUE INTRODUDEIXIS NOM, HORES, DESCRIPCIO I COMPLETED")
        
        resp.status = falcon.HTTP_200
'''




@falcon.before(requires_auth)
class ResourceCreateTask(DAMCoreResource):
    def on_post(self,req,resp,*args,**kwargs):
        super(ResourceCreateTask, self).on_post(req,resp,*args,**kwargs)
        
        task = Task()
        #Request Body --> {tittle:value1, description:value2} raw-json
        
        try:
            	task.name = req.get_param("name") #NOM DE LA CLAU QUE VA AL BODY DEL POSTMAN, si fessim req.get_param("KEY") podriem fer postman amb Params
            	task.description = req.get_param("description")	    
	    	task.hours = req.get_param("hours")
	    	task.completed = req.get_param("completed")
            	self.db_session.add(task)
            	try:
                	self.db_session.commit()
            	except IntegrityError:
                	raise falcon.HTTPBadRequest("LA TASCA EXISTEIX JA")               
        except KeyError:
            	raise falcon.HTTPBadRequest("PER PODER FER UN LLIBRE NECESSITO MÍNIM QUE INTRODUDEIXIS NOM, HORES, DESCRIPCIO I COMPLETED")
        
        resp.status = falcon.HTTP_200





class ResourceGetTask(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetTask, self).on_get(req,resp,*args,**kwargs)
        
        tasks = list()
        _query = self.db_session.query(Task) #BUSCA TOT EL QUE HI HAGI A LA BASE DE DADES A LA TAULA BOOK I POSAU A query
               
        '''#filter
        genres = req.get_param("genres")'''
        
        '''if genres is not None:
            _query = _query.filter(Book.genre == genres)       
        results = _query.all()'''    
        results = query.all()#retornam tot el que hi hagi a query
        '''results = query.limit(3)#retornam nomes 3'''            
        for task in results:
            tasks.append(tasks.json_model) #Si enlloc de custom escribissim 
            
        resp.media = tasks #enviem tot l'array de les tasques amb el model json definit a models







