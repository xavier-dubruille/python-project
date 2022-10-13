#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: Customer
#------------------------------------------------------------

CREATE TABLE Customer(
        idCusto       Int  Auto_increment  NOT NULL ,
        nameCusto     Varchar (250) NOT NULL ,
        lastnameCusto Varchar (250) NOT NULL
	,CONSTRAINT Customer_PK PRIMARY KEY (idCusto)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Brand
#------------------------------------------------------------

CREATE TABLE Brand(
        idBrand   Int  Auto_increment  NOT NULL ,
        nameBrand Varchar (250) NOT NULL
	,CONSTRAINT Brand_PK PRIMARY KEY (idBrand)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Motor
#------------------------------------------------------------

CREATE TABLE Motor(
        idMotor   Int  Auto_increment  NOT NULL ,
        nameMotor Varchar (250) NOT NULL
	,CONSTRAINT Motor_PK PRIMARY KEY (idMotor)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Car
#------------------------------------------------------------

CREATE TABLE Car(
        idCar              Int  Auto_increment  NOT NULL ,
        stockDateCar       Date ,
        techControlDateCar Date ,
        rentedCar          Bool NOT NULL ,
        idBrand            Int NOT NULL ,
        idMotor            Int NOT NULL
	,CONSTRAINT Car_PK PRIMARY KEY (idCar)

	,CONSTRAINT Car_Brand_FK FOREIGN KEY (idBrand) REFERENCES Brand(idBrand)
	,CONSTRAINT Car_Motor0_FK FOREIGN KEY (idMotor) REFERENCES Motor(idMotor)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Reservation
#------------------------------------------------------------

CREATE TABLE Reservation(
        idRes   Int  Auto_increment  NOT NULL ,
        idCar   Int NOT NULL ,
        idCusto Int NOT NULL
	,CONSTRAINT Reservation_PK PRIMARY KEY (idRes)

	,CONSTRAINT Reservation_Car_FK FOREIGN KEY (idCar) REFERENCES Car(idCar)
	,CONSTRAINT Reservation_Customer0_FK FOREIGN KEY (idCusto) REFERENCES Customer(idCusto)
)ENGINE=InnoDB;

