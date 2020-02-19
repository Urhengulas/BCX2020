import React, { useState } from "react";
import "./App.css";
import { Form, Button, Row, Card, Icon } from "antd";
import { Formik } from "formik";
import { FormItem, DatePicker, Select } from "formik-antd";
import { Typography } from "antd";
import axios from "axios";

const { Title, Text } = Typography;

const App = () => {
  const [result, setResult] = useState(new Date());
  let [flag, setFlag] = useState(false);

  const makeRequest = async (
    startTime: Date,
    endTime: Date,
    productionTime: number
  ) => {
    console.log(startTime);
    const startTimeStr = `${startTime.getFullYear()}-${startTime.getMonth() +
      1}-${startTime.getDate()} ${startTime.getHours()}:${startTime.getMinutes()}:${startTime.getSeconds()}`;
    const endTimeStr = `${endTime.getFullYear()}-${endTime.getMonth() +
      1}-${endTime.getDate()} ${endTime.getHours()}:${endTime.getMinutes()}:${endTime.getSeconds()}`;
    const inputData = {
      earliest_start_time: startTimeStr,
      deadline: endTimeStr,
      prod_time_in_min: productionTime
    };
    console.log("inputData=", inputData);
    const res = await axios.post("http://localhost:5000/schedule", inputData);
    const a = res.data.start_time;
    console.log("result=", a);
    setResult(new Date(a));
    setFlag(true);
  };

  return (
    <div
      className="App"
      style={{
        textAlign: "center",
        height: "100vh",
        display: "flex",
        alignItems: "center"
      }}
    >
      <Row style={{ margin: "0 auto" }}>
        <Icon type="dot-chart" style={{ fontSize: 80, color: "#1DA57A" }} />
        <Title>Zero Emissions Factory</Title>
        <Text>Input your conditions</Text>
        {
          <Formik
            initialValues={{
              startTime: new Date(2019, 5, 10, 10, 0),
              endTime: new Date(2019, 5, 10, 15, 0),
              productionTime: 0 //minutes
            }}
            onSubmit={async (values: any, actions: any) => {
              actions.setSubmitting(true);
              if (values) {
                const { startTime, endTime, productionTime } = values;
                // console.log(typeof startTime, " : ", typeof endTime);
                // return false;
                makeRequest(
                  typeof startTime === "string"
                    ? new Date(startTime)
                    : startTime,
                  typeof endTime === "string" ? new Date(endTime) : endTime,
                  productionTime
                );
                actions.setSubmitting(false);
              }
            }}
            render={({ handleSubmit, isSubmitting, isValid }) => (
              <Form onSubmit={handleSubmit}>
                <FormItem name="startTime" label="Start Time">
                  <DatePicker
                    showTime
                    name="startTime"
                    style={{ width: 200 }}
                    format="YYYY-MM-DD HH:mm"
                  />
                </FormItem>
                <FormItem name="endTime" label="End Time">
                  <DatePicker
                    showTime
                    name="endTime"
                    style={{ width: 200 }}
                    format="YYYY-MM-DD HH:mm"
                  />
                </FormItem>
                <FormItem
                  name="productionTime"
                  label="Approximate Production Time"
                >
                  <Select name="productionTime" style={{ width: 200 }}>
                    {Select.renderOptions(
                      [15, 30, 45, 60].map(duration => ({
                        value: duration,
                        label: <span>{duration.toString() + " minutes"}</span>
                      }))
                    )}
                  </Select>
                </FormItem>
                <Form.Item>
                  <Button
                    icon="check"
                    type="primary"
                    style={{ background: "#1DA57A", border: "#1DA57A" }}
                    loading={isSubmitting}
                    disabled={!isValid}
                    onClick={() => {
                      handleSubmit();
                    }}
                  >
                    Optimize production
                  </Button>
                </Form.Item>
              </Form>
            )}
          />
        }
        {flag === true ? (
          <Card
            title="Found optimal solutions"
            headStyle={{ backgroundColor: "#1DA57A" }}
            bodyStyle={{ backgroundColor: "#6af2c2" }}
          >
            {String(result)}
          </Card>
        ) : (
          <div></div>
        )}
      </Row>
    </div>
  );
};

export default App;
