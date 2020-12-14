-- MySQL Script generated by MySQL Workbench
-- Mon Nov 23 14:41:13 2020
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
-- Table `mydb`.`Star`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Star` (
  `idStar` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `birthYear` YEAR NOT NULL,
  `deathYear` YEAR NULL,
  PRIMARY KEY (`idStar`),
  UNIQUE INDEX `Ime_UNIQUE` (`Name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Title`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Title` (
  `idTitle` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(10) NOT NULL,
  `mainTitle` VARCHAR(45) NOT NULL,
  `originalTitle` VARCHAR(45) NOT NULL,
  `adult` TINYINT(1) NOT NULL,
  `releaseYear` YEAR NOT NULL,
  `endYear` YEAR NULL,
  `lengthMinutes` INT NOT NULL,
  `avgRating` FLOAT NULL,
  `numberOfVotes` INT NOT NULL,
  PRIMARY KEY (`idTitle`),
  UNIQUE INDEX `glavniNaslov_UNIQUE` (`mainTitle` ASC),
  UNIQUE INDEX `prvotniNaslov_UNIQUE` (`originalTitle` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Genre` (
  `idGenre` INT NOT NULL AUTO_INCREMENT,
  `genreName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idGenre`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`otherTitles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`otherTitles` (
  `idOtherTitles` INT NOT NULL AUTO_INCREMENT,
  `titleLocal` VARCHAR(45) NOT NULL,
  `region` VARCHAR(45) NOT NULL,
  `language` VARCHAR(45) NULL,
  `isOriginal` TINYINT(1) NOT NULL,
  `idTitle` INT NOT NULL,
  PRIMARY KEY (`idOtherTitles`, `idTitle`),
  INDEX `fk_otherTitles_Title1_idx` (`idTitle` ASC),
  CONSTRAINT `fk_otherTitles_Title1`
    FOREIGN KEY (`idTitle`)
    REFERENCES `mydb`.`Title` (`idTitle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Role` (
  `idRole` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NULL,
  `starredAs` VARCHAR(45) NULL,
  `idStar` INT NOT NULL,
  `idTitle` INT NOT NULL,
  PRIMARY KEY (`idRole`, `idStar`, `idTitle`),
  INDEX `fk_Role_Star1_idx` (`idStar` ASC),
  INDEX `fk_Role_Title1_idx` (`idTitle` ASC),
  CONSTRAINT `fk_Role_Star1`
    FOREIGN KEY (`idStar`)
    REFERENCES `mydb`.`Star` (`idStar`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Role_Title1`
    FOREIGN KEY (`idTitle`)
    REFERENCES `mydb`.`Title` (`idTitle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`MainTeam`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`MainTeam` (
  `idMainTeam` INT NOT NULL AUTO_INCREMENT,
  `director` TINYINT(1) NULL,
  `writer` TINYINT(1) NULL,
  `idTitle` INT NOT NULL,
  `idStar` INT NOT NULL,
  PRIMARY KEY (`idMainTeam`, `idTitle`, `idStar`),
  INDEX `fk_MainTeam_Title1_idx` (`idTitle` ASC),
  INDEX `fk_MainTeam_Star1_idx` (`idStar` ASC),
  CONSTRAINT `fk_MainTeam_Title1`
    FOREIGN KEY (`idTitle`)
    REFERENCES `mydb`.`Title` (`idTitle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MainTeam_Star1`
    FOREIGN KEY (`idStar`)
    REFERENCES `mydb`.`Star` (`idStar`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Episode`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Episode` (
  `idEpisode` INT NOT NULL AUTO_INCREMENT,
  `seasonNumber` INT NOT NULL,
  `episodeNumber` INT NOT NULL,
  `idTitle` INT NOT NULL,
  PRIMARY KEY (`idEpisode`, `idTitle`),
  INDEX `fk_Episode_Title1_idx` (`idTitle` ASC),
  CONSTRAINT `fk_Episode_Title1`
    FOREIGN KEY (`idTitle`)
    REFERENCES `mydb`.`Title` (`idTitle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(70) NOT NULL,
  `email` VARCHAR(45) NULL,
  `phone` VARCHAR(12) NULL,
  PRIMARY KEY (`idUser`),
  UNIQUE INDEX `uporabniskoIme_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  UNIQUE INDEX `tel_UNIQUE` (`phone` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Watched`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Watched` (
  `comment` TEXT NULL,
  `rating` TINYINT(10) NULL DEFAULT 0,
  `idUser` INT NOT NULL,
  `idTitle` INT NOT NULL,
  PRIMARY KEY (`idUser`, `idTitle`),
  INDEX `fk_Watched_Title1_idx` (`idTitle` ASC),
  CONSTRAINT `fk_Watched_User1`
    FOREIGN KEY (`idUser`)
    REFERENCES `mydb`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Watched_Title1`
    FOREIGN KEY (`idTitle`)
    REFERENCES `mydb`.`Title` (`idTitle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`GenreAndTitle`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`GenreAndTitle` (
  `idTitle` INT NOT NULL,
  `idGenre` INT NOT NULL,
  PRIMARY KEY (`idTitle`, `idGenre`),
  INDEX `fk_Title_has_Genre_Genre1_idx` (`idGenre` ASC),
  INDEX `fk_Title_has_Genre_Title1_idx` (`idTitle` ASC),
  CONSTRAINT `fk_Title_has_Genre_Title1`
    FOREIGN KEY (`idTitle`)
    REFERENCES `mydb`.`Title` (`idTitle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Title_has_Genre_Genre1`
    FOREIGN KEY (`idGenre`)
    REFERENCES `mydb`.`Genre` (`idGenre`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;