Храним запросы на создание процедур


CREATE TRIGGER check_update
    AFTER INSERT ON receipts
    FOR EACH ROW
    EXECUTE FUNCTION update_typeproducts();

