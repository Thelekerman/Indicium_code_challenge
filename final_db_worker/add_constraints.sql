--
-- Name: fk_order_details_orders; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY order_details
    ADD CONSTRAINT fk_order_details_orders FOREIGN KEY (order_id) REFERENCES orders;


--
-- Name: fk_order_details_products; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY order_details
    ADD CONSTRAINT fk_order_details_products FOREIGN KEY (product_id) REFERENCES products;


--
-- Name: fk_orders_customers; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY orders
    ADD CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id) REFERENCES customers;


--
-- Name: fk_orders_employees; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY orders
    ADD CONSTRAINT fk_orders_employees FOREIGN KEY (employee_id) REFERENCES employees;


--
-- Name: fk_orders_shippers; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY orders
    ADD CONSTRAINT fk_orders_shippers FOREIGN KEY (ship_via) REFERENCES shippers;


--
-- Name: fk_products_categories; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY products
    ADD CONSTRAINT fk_products_categories FOREIGN KEY (category_id) REFERENCES categories;


--
-- Name: fk_products_suppliers; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY products
    ADD CONSTRAINT fk_products_suppliers FOREIGN KEY (supplier_id) REFERENCES suppliers;


--
-- Name: fk_territories_region; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY territories
    ADD CONSTRAINT fk_territories_region FOREIGN KEY (region_id) REFERENCES region;


--
-- Name: fk_employee_territories_territories; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY employee_territories
    ADD CONSTRAINT fk_employee_territories_territories FOREIGN KEY (territory_id) REFERENCES territories;


--
-- Name: fk_employee_territories_employees; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY employee_territories
    ADD CONSTRAINT fk_employee_territories_employees FOREIGN KEY (employee_id) REFERENCES employees;


--
-- Name: fk_customer_customer_demo_customer_demographics; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY customer_customer_demo
    ADD CONSTRAINT fk_customer_customer_demo_customer_demographics FOREIGN KEY (customer_type_id) REFERENCES customer_demographics;


--
-- Name: fk_customer_customer_demo_customers; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY customer_customer_demo
    ADD CONSTRAINT fk_customer_customer_demo_customers FOREIGN KEY (customer_id) REFERENCES customers;


--
-- Name: fk_employees_employees; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY employees
    ADD CONSTRAINT fk_employees_employees FOREIGN KEY (reports_to) REFERENCES employees;

    
--
-- PostgreSQL database dump complete
--
