#!/usr/bin/python
# -*- encoding: utf-8 -*-
from typing import List
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    Text,
    Float,
    Date,
    Boolean,
)
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from config.connection_db import Base


class User(Base):
    __tablename__ = "Tb_user"

    pk_user = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    password = Column(Text)
    email = Column(String(50))
    cep = Column(String(10))
    city = Column(String(25))
    address = Column(String(30))
    neighborhood = Column(String(30))
    cellphone = Column(String(25))
    user_token = Column(String(16))
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_employee = Column(Boolean, nullable=False, default=False)

    # Add a one-to-one relationship
    authentication: Mapped["Authentication"] = relationship()
    # Add a one-to-many relationship
    order: Mapped["Order"] = relationship()


class Authentication(Base):
    __tablename__ = "Tb_authentication"

    id = Column(Integer, primary_key=True, autoincrement=True)
    access_token = Column(Text)
    expiration = Column(DateTime)

    # Add a one-to-one relationship
    fk_user: Mapped[int] = mapped_column(ForeignKey("Tb_user.pk_user"))


class Product(Base):
    __tablename__ = "Tb_product"

    pk_product = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(Text)
    value = Column(Float)
    stok = Column(Integer)
    thumbnail = Column(Text, default=None)

    # Add a one-to-Many relationship
    fk_product_file: Mapped[List["ProductFile"]] = relationship()
    fk_order_product: Mapped["OrderProduct"] = relationship()


class ProductFile(Base):
    __tablename__ = "Tb_product_file"

    pk_product_file = Column(Integer, primary_key=True, autoincrement=True)
    file_code = Column(Text)

    # Add a one-to-Many relationship
    fk_product: Mapped[int] = mapped_column(ForeignKey("Tb_product.pk_product"))


class DeliveryType(Base):
    __tablename__ = "Tb_delivery_type"

    pk_delivery_type = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(Text)

    # Add a one-to-one relationship
    delivery: Mapped["Delivery"] = relationship()


class Delivery(Base):
    __tablename__ = "Tb_delivery"

    pk_delivery = Column(Integer, primary_key=True, autoincrement=True)
    cep = Column(String(50))
    city = Column(String(50))
    address = Column(String(50))
    neighborhood = Column(String(50))
    number = Column(Integer)

    # Add a one-to-one relationship
    fk_delivery_type: Mapped[int] = mapped_column(
        ForeignKey("Tb_delivery_type.pk_delivery_type")
    )

    order_summary: Mapped["OrderSummary"] = relationship()


class PaymentType(Base):
    __tablename__ = "Tb_payment_type"

    pk_payment_type = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(Text)

    # Add a one-to-one relationship
    payment: Mapped["Payment"] = relationship()


class Payment(Base):
    __tablename__ = "Tb_payment"

    pk_payment = Column(Integer, primary_key=True, autoincrement=True)
    card_name = Column(Text)
    card_number = Column(String(30))
    data_expiration = Column(Date)
    total_value = Column(Float)
    status = Column(Integer)

    # Add a one-to-one relationship
    fk_payment_type: Mapped[int] = mapped_column(
        ForeignKey("Tb_payment_type.pk_payment_type")
    )

    order_summary: Mapped["OrderSummary"] = relationship()


class OrderProduct(Base):
    __tablename__ = "Tb_order_product"

    pk_order_product = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    total_value = Column(Float)

    # Add a one-to-one relationship
    fk_order: Mapped[int] = mapped_column(ForeignKey("Tb_order.pk_order"))

    fk_product: Mapped[int] = mapped_column(ForeignKey("Tb_product.pk_product"))


class Order(Base):
    __tablename__ = "Tb_order"

    pk_order = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Integer)

    # Add a one-to-one relationship
    fk_user: Mapped[int] = mapped_column(ForeignKey("Tb_user.pk_user"))
    order_summary: Mapped["OrderSummary"] = relationship()
    fk_order_product: Mapped["OrderProduct"] = relationship()


class OrderSummary(Base):
    __tablename__ = "Tb_order_summary"

    pk_order_summary = Column(Integer, primary_key=True, autoincrement=True)
    order_code = Column(String(36))
    created = Column(DateTime)
    status = Column(Integer)

    # Add a one-to-one relationship
    fk_order: Mapped[int] = mapped_column(ForeignKey("Tb_order.pk_order"))

    fk_payment: Mapped[int] = mapped_column(ForeignKey("Tb_payment.pk_payment"))

    fk_delivery: Mapped[int] = mapped_column(ForeignKey("Tb_delivery.pk_delivery"))
