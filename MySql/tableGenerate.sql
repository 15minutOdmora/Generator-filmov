-- MySQL Script generated by MySQL Workbench
-- Thu Jan 14 15:59:11 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(80) NOT NULL,
  `email` VARCHAR(50) NULL,
  `phoneNumber` VARCHAR(50) NULL,
  PRIMARY KEY (`idUser`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  UNIQUE INDEX `phoneNumber_UNIQUE` (`phoneNumber` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Genre` (
  `idGenre` INT NOT NULL,
  `genreName` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`idGenre`),
  UNIQUE INDEX `genre_UNIQUE` (`genreName` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Movie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Movie` (
  `idMovie` VARCHAR(40) NOT NULL,
  `title` VARCHAR(1000) NOT NULL,
  `isAdult` TINYINT(1) NOT NULL,
  `releaseYear` INT NULL,
  `runtimeMinutes` INT NULL,
  `rating` FLOAT NULL,
  `numVotes` INT NULL,
  PRIMARY KEY (`idMovie`),
  UNIQUE INDEX `Title_UNIQUE` (`title` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`WritersAndDirectors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`WritersAndDirectors` (
  `idWritersAndDirectors` VARCHAR(40) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `birthYear` INT NULL,
  `deathYear` INT NULL,
  PRIMARY KEY (`idWritersAndDirectors`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`GenresByMovie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`GenresByMovie` (
  `idGenre` INT NOT NULL,
  `idMovie` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idGenre`, `idMovie`),
  INDEX `fk_Genre_has_Movies_Movies1_idx` (`idMovie` ASC),
  INDEX `fk_Genre_has_Movies_Genre_idx` (`idGenre` ASC),
  CONSTRAINT `fk_Genre_has_Movies_Genre`
    FOREIGN KEY (`idGenre`)
    REFERENCES `mydb`.`Genre` (`idGenre`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Genre_has_Movies_Movies1`
    FOREIGN KEY (`idMovie`)
    REFERENCES `mydb`.`Movie` (`idMovie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Opinion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Opinion` (
  `idUser` INT NOT NULL,
  `idMovie` VARCHAR(45) NOT NULL,
  `ocena` FLOAT NULL,
  `opinion` VARCHAR(500) NULL,
  PRIMARY KEY (`idUser`, `idMovie`),
  INDEX `fk_User_has_Movies_Movies1_idx` (`idMovie` ASC),
  INDEX `fk_User_has_Movies_User1_idx` (`idUser` ASC),
  CONSTRAINT `fk_User_has_Movies_User1`
    FOREIGN KEY (`idUser`)
    REFERENCES `mydb`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_Movies_Movies1`
    FOREIGN KEY (`idMovie`)
    REFERENCES `mydb`.`Movie` (`idMovie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Team` (
  `idWritersAndDirectors` VARCHAR(45) NOT NULL,
  `idMovie` VARCHAR(45) NOT NULL,
  `director` TINYINT(1) NULL,
  `writer` TINYINT(1) NULL,
  PRIMARY KEY (`idWritersAndDirectors`, `idMovie`),
  INDEX `fk_WritersAndDirectors_has_Movies_Movies1_idx` (`idMovie` ASC),
  INDEX `fk_WritersAndDirectors_has_Movies_WritersAndDirectors1_idx` (`idWritersAndDirectors` ASC),
  CONSTRAINT `fk_WritersAndDirectors_has_Movies_WritersAndDirectors1`
    FOREIGN KEY (`idWritersAndDirectors`)
    REFERENCES `mydb`.`WritersAndDirectors` (`idWritersAndDirectors`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_WritersAndDirectors_has_Movies_Movies1`
    FOREIGN KEY (`idMovie`)
    REFERENCES `mydb`.`Movie` (`idMovie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
