package it.univaq.disim.sealabaq;


import io.opentracing.Span;
import io.opentracing.Tracer;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.web.servlet.handler.HandlerInterceptorAdapter;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Random;

public class LatencyInjectionInterceptor extends HandlerInterceptorAdapter {

    private static final Log logger = LogFactory.getLog(LatencyInjectionInterceptor.class);

    private static final String tagKey = "experiment";

    private static final Random random = new Random(33);

    private static final int randomBound = 10;


    private Tracer tracer;

    public LatencyInjectionInterceptor(Tracer tracer) {
        this.tracer = tracer;
    }

    private String randomNumber() {
        return Integer.toString(random.nextInt(randomBound));
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        logger.info("Adding experiment tag");

        Span span = tracer.activeSpan();
        if (span != null) {
            if (span.getBaggageItem(tagKey) == null){
                span.setBaggageItem(tagKey, randomNumber());
            }
            span.setTag(tagKey, span.getBaggageItem(tagKey));
        }

        return true;
    }

}
