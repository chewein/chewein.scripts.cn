

class	Student(object):

	def __init__(self,name,score):
         self.name = name 
         self.score= score
    
	def print_score(self):
         print '%s : %s' %(self.name,self.score)


bar = Student('chewein','98');
bar.print_score();

class	Student_private(object):

    def __init__(self,name,score):
         self.__name = name;
         self.__score= score;

    def print_score(self):
         print '%s : %s' %(self.__name,self.__score)

    def set_score(self,score):
         self.__score= score;

    def get_score(self):	 
         return self.__score 

    def get_name(self):	 
         return self.__name 


bar = Student_private('chewein','98');
bar.print_score()
bar.__name = 'chengwei' #wrong,__name is private data, only can access by method  


